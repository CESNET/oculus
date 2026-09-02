import json
from pathlib import Path

import docker
from docker.errors import DockerException

from .processor import Processor
from .visualization_helper import ProcessingPlan, VisualizationTask
from ...domain import (
    OutputFormat,
    ProcessorOutput,
    TileGroup,
)
from ...settings import settings

FORMAT_FLAGS = {
    OutputFormat.JPG: {
        TileGroup.FULL_PRODUCT: "-J",
        TileGroup.WM_TILES: "-j",
    },
    OutputFormat.PNG: {
        TileGroup.FULL_PRODUCT: "-P",
        TileGroup.WM_TILES: "-p",
    },
    OutputFormat.WEBP: {
        TileGroup.FULL_PRODUCT: "-W",
        TileGroup.WM_TILES: "-w",
    },
}


class GJTIFFProcessor(Processor):
    _GJTIFF_CONTAINER_NAME = "oculus_gjtiff"

    def _process(
            self,
            processing_plan: ProcessingPlan,
    ) -> list[ProcessorOutput]:

        quality = self._validate_quality(
            self._job.request_properties.get("quality"),
        )

        zoom_levels = self._validate_zoom_levels(
            self._job.request_properties.get("zoom_levels"),
        )

        command = self._build_command(
            processing_plan=processing_plan,
            quality=quality,
            zoom_levels=zoom_levels,
        )

        container = self._get_container()

        gjtiff_stdout = self._run_command(
            container=container,
            command=command,
        )

        return self._normalize_outputs(
            processing_plan=processing_plan,
            gjtiff_stdout=gjtiff_stdout,
            zoom_levels=zoom_levels,
        )

    # ------------------------------------------------------------------
    # command
    # ------------------------------------------------------------------

    def _build_command(
            self,
            processing_plan: ProcessingPlan,
            quality: int,
            zoom_levels: list[int],
    ) -> list[str]:

        visualization_inputs = [
            self._build_visualization_input(task)
            for task in processing_plan.visualizations
        ]

        format_flags = self._build_format_flags(
            processing_plan.outputs,
        )

        processed_directory = self._feature_state.feature_root_directory / "processed"

        processed_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return [
            "gjtiff",
            "-q",
            str(quality),
            "-Q",
            "-z",
            ",".join(map(str, zoom_levels)),
            "-o",
            str(processed_directory),
            *format_flags,
            *visualization_inputs,
        ]

    @staticmethod
    def _build_visualization_input(
            task: VisualizationTask,
    ) -> str:

        input_files = ",".join(
            str(path)
            for path in task.input_files
        )

        if task.prefix is not None:
            return f"{task.prefix}@{input_files}"

        return input_files

    @staticmethod
    def _build_format_flags(
            outputs: dict[OutputFormat, set[TileGroup]],
    ) -> list[str]:

        flags: list[str] = []

        for format_name, groups in outputs.items():

            if format_name not in FORMAT_FLAGS:
                raise ValueError(f"Unsupported output format: {format_name}")

            for group in groups:

                flag = FORMAT_FLAGS[format_name].get(group)

                if flag is None:
                    raise ValueError(f"Unsupported output combination: {format_name}/{group}")

                flags.append(flag)

        return flags

    # ------------------------------------------------------------------
    # output normalization
    # ------------------------------------------------------------------

    def _normalize_outputs(
            self,
            processing_plan: ProcessingPlan,
            gjtiff_stdout: str,
            zoom_levels: list[int],
    ) -> list[ProcessorOutput]:

        full_product_outputs = self._normalize_full_products(
            processing_plan=processing_plan,
            gjtiff_stdout=gjtiff_stdout,
        )

        wm_tile_outputs = self._normalize_wm_tiles(
            processing_plan=processing_plan,
            zoom_levels=zoom_levels,
        )

        normalized_outputs = [
            *full_product_outputs,
            *wm_tile_outputs,
        ]

        self._logger.info(f"GJTIFF normalized outputs: {normalized_outputs}")

        return normalized_outputs

    # ------------------------------------------------------------------
    # full products
    # ------------------------------------------------------------------

    def _normalize_full_products(
            self,
            processing_plan: ProcessingPlan,
            gjtiff_stdout: str,
    ) -> list[ProcessorOutput]:

        try:
            outputs = json.loads(gjtiff_stdout)

        except json.JSONDecodeError as exc:
            raise RuntimeError("Unable to parse GJTIFF stdout as JSON") from exc

        if not isinstance(outputs, list):
            raise RuntimeError(f"Unexpected GJTIFF stdout format: expected list, got {type(outputs).__name__}")

        normalized_outputs: list[ProcessorOutput] = []

        for output in outputs:

            input_file = output.get("infile")
            output_file = output.get("outfile")

            if not input_file or not output_file:
                self._logger.warning(f"Invalid GJTIFF output: {output}")
                continue

            task = self._find_task(
                processing_plan=processing_plan,
                input_file=input_file,
            )

            if task is None:
                self._logger.warning(f"Unable to match GJTIFF output to visualization task: {output}")
                continue

            output_file = Path(output_file)

            normalized_path = self._normalize_output_path(
                outfile=output_file,
                task=task,
            )

            if output_file != normalized_path:
                output_file.rename(normalized_path)

            normalized_outputs.append(
                ProcessorOutput(
                    visualization_id=task.id,
                    group=TileGroup.FULL_PRODUCT,
                    format_name=self._get_output_format(normalized_path),
                    path=normalized_path,
                )
            )

        return normalized_outputs

    # ------------------------------------------------------------------
    # WM tiles
    # ------------------------------------------------------------------

    def _normalize_wm_tiles(
            self,
            processing_plan: ProcessingPlan,
            zoom_levels: list[int],
    ) -> list[ProcessorOutput]:

        normalized_outputs: list[ProcessorOutput] = []

        wm_tile_formats = self._get_wm_tile_formats(
            processing_plan=processing_plan,
        )

        if not wm_tile_formats:
            return normalized_outputs

        processed_directory = self._feature_state.feature_root_directory / "processed"

        for task in processing_plan.visualizations:

            # GJTIFF creates the directory using its own naming convention.
            gjtiff_tiles_path = processed_directory / self._get_gjtiff_output_stem(task)

            # Application uses the canonical visualization ID.
            normalized_tiles_path = processed_directory / task.id

            if not self._has_wm_tiles(
                    path=gjtiff_tiles_path,
                    zoom_levels=zoom_levels,
            ):
                self._logger.warning(
                    f"Expected WM tiles were not generated for visualization '{task.id}': {gjtiff_tiles_path}"
                )
                continue

            # Rename GJTIFF's directory to our canonical visualization ID.
            if gjtiff_tiles_path != normalized_tiles_path:

                if normalized_tiles_path.exists():
                    raise RuntimeError(
                        f"Cannot rename WM tiles directory because destination already exists: {normalized_tiles_path}"
                    )

                gjtiff_tiles_path.rename(normalized_tiles_path)

            for format_name in wm_tile_formats:
                normalized_outputs.append(
                    ProcessorOutput(
                        visualization_id=task.id,
                        group=TileGroup.WM_TILES,
                        format_name=format_name,
                        path=normalized_tiles_path,
                        zoom_levels=tuple(zoom_levels),
                    )
                )

        return normalized_outputs

    @staticmethod
    def _get_wm_tile_formats(
            processing_plan: ProcessingPlan,
    ) -> set[OutputFormat]:

        return {
            format_name
            for format_name, groups
            in processing_plan.outputs.items()
            if TileGroup.WM_TILES in groups
        }

    def _get_wm_tiles_path(
            self,
            task: VisualizationTask,
    ) -> Path:

        processed_directory = self._feature_state.feature_root_directory / "processed"

        output_stem = self._get_gjtiff_output_stem(task=task)

        return processed_directory / output_stem

    @staticmethod
    def _get_gjtiff_output_stem(
            task: VisualizationTask,
    ) -> str:

        input_names = "-COMMA-".join(
            path.stem
            for path in task.input_files
        )

        if task.prefix is not None:
            return f"{task.prefix}-{input_names}"

        return input_names

    @staticmethod
    def _has_wm_tiles(
            path: Path,
            zoom_levels: list[int],
    ) -> bool:

        if not path.is_dir():
            return False

        return all(
            (path / str(zoom)).is_dir()
            for zoom in zoom_levels
        )

    # ------------------------------------------------------------------
    # task matching
    # ------------------------------------------------------------------

    @classmethod
    def _find_task(
            cls,
            processing_plan: ProcessingPlan,
            input_file: str,
    ) -> VisualizationTask | None:

        for task in processing_plan.visualizations:

            actual_inputs = cls._get_gjtiff_inputs(
                infile=input_file,
                prefix=task.prefix,
            )

            expected_inputs = cls._get_input_identifiers(
                task.input_files,
            )

            if actual_inputs == expected_inputs:
                return task

        return None

    @staticmethod
    def _get_gjtiff_inputs(
            infile: str,
            prefix: str | None,
    ) -> tuple[str, ...]:

        parts = Path(infile).name.split("-COMMA-")

        if prefix is not None:

            prefix_separator = f"{prefix}-"

            if not parts[0].startswith(prefix_separator):
                return ()

            parts[0] = parts[0][len(prefix_separator):]

        return tuple(
            Path(part).stem
            for part in parts
            if part
        )

    @staticmethod
    def _get_input_identifiers(
            input_files: tuple[Path, ...],
    ) -> tuple[str, ...]:

        return tuple(
            path.stem
            for path in input_files
        )

    # ------------------------------------------------------------------
    # path / format
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_output_path(
            outfile: Path,
            task: VisualizationTask,
    ) -> Path:

        return outfile.with_name(
            f"{task.id}{outfile.suffix}"
        )

    @staticmethod
    def _get_output_format(
            path: Path,
    ) -> OutputFormat:

        try:
            return OutputFormat(
                path.suffix.lstrip(".").lower()
            )

        except ValueError as exc:
            raise ValueError(f"Unsupported GJTIFF output format: {path}") from exc

    # ------------------------------------------------------------------
    # validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_quality(
            value,
    ) -> int:

        if value is None:
            return settings.DEFAULT_PROCESSING_QUALITY

        try:
            quality = int(value)

        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid quality: {value}") from exc

        if not 0 <= quality <= 100:
            raise ValueError(f"Quality must be between 0 and 100, got {quality}")

        return quality

    @staticmethod
    def _validate_zoom_levels(
            value,
    ) -> list[int]:

        if value is None:
            return list(
                settings.DEFAULT_PROCESSING_ZOOM_LEVELS
            )

        if isinstance(value, str):
            value = value.split(",")

        try:
            zoom_levels = [
                int(level)
                for level in value
            ]

        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid zoom levels: {value}") from exc

        if any(level < 0 for level in zoom_levels):
            raise ValueError(f"Zoom levels must be non-negative: {zoom_levels}")

        return zoom_levels

    # ------------------------------------------------------------------
    # docker
    # ------------------------------------------------------------------

    def _get_container(self):

        client = docker.from_env()

        try:
            return client.containers.get(
                self._GJTIFF_CONTAINER_NAME
            )

        except DockerException as exc:
            raise RuntimeError(
                "GJTIFF container "
                f"'{self._GJTIFF_CONTAINER_NAME}' not found. "
                f"Error: {exc}"
            ) from exc

    def _run_command(
            self,
            container,
            command: list[str],
    ) -> str:

        self._logger.info(f"Running GJTIFF command: {' '.join(command)}")

        exec_result = container.exec_run(
            cmd=command,
            stdout=True,
            stderr=True,
            tty=False,
            demux=True,
        )

        stdout, stderr = exec_result.output

        if exec_result.exit_code != 0:
            error = (
                stderr.decode("utf-8")
                if stderr
                else "Unknown error"
            )

            raise RuntimeError(f"GJTIFF failed with exit code {exec_result.exit_code}: {error}")

        stdout_text = (
            stdout.decode("utf-8")
            if stdout
            else ""
        )

        if stdout_text:
            self._logger.info(f"GJTIFF output: {stdout_text}")

        return stdout_text
