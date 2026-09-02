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

    def _build_command(
            self,
            processing_plan: ProcessingPlan,
            quality: int,
            zoom_levels: list[int],
    ) -> list[str]:

        visualization_inputs: list[str] = []

        for task in processing_plan.visualizations:

            input_files = ",".join(
                str(path)
                for path in task.input_files
            )

            if task.prefix:
                visualization_inputs.append(
                    f"{task.id.upper()}@{input_files}"
                )
            else:
                visualization_inputs.append(
                    input_files
                )

        format_flags = self._build_format_flags(
            processing_plan.outputs,
        )

        processed_directory = self._feature_state.feature_root_directory / "processed"

        processed_directory.mkdir(parents=True, exist_ok=True)

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

    def _normalize_outputs(
            self,
            processing_plan: ProcessingPlan,
            gjtiff_stdout: str,
            zoom_levels: list[int],
    ) -> list[ProcessorOutput]:

        outputs = json.loads(gjtiff_stdout)

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

            if normalized_path != output_file:
                output_file.rename(normalized_path)

            normalized_outputs.append(
                ProcessorOutput(
                    visualization_id=task.id,
                    group=TileGroup.FULL_PRODUCT,
                    format_name=self._get_output_format(
                        normalized_path
                    ),
                    path=normalized_path,
                    zoom_levels=zoom_levels,
                )
            )

        self._logger.info(f"GJTIFF normalized outputs: {normalized_outputs}")

        return normalized_outputs

    @classmethod
    def _find_task(
            cls,
            processing_plan: ProcessingPlan,
            input_file: str,
    ) -> VisualizationTask | None:

        gjtiff_prefix, gjtiff_inputs = (
            cls._parse_gjtiff_infile(input_file)
        )

        for task in processing_plan.visualizations:
            task_inputs = cls._get_input_identifiers(
                task.input_files
            )

            if task_inputs != gjtiff_inputs:
                continue

            if task.prefix != gjtiff_prefix:
                continue

            return task

        return None

    @staticmethod
    def _parse_gjtiff_infile(
            infile: str,
    ) -> tuple[str | None, tuple[str, ...]]:

        name = Path(infile).name

        parts = name.split("-COMMA-")

        if not parts:
            return None, ()

        first = parts[0]

        prefix = None

        # GJTIFF prefix is separated from the first input
        # by a single '-'.
        #
        # Example:
        #   NDVI-T33..._B08-COMMA-T33..._B04
        #
        # becomes:
        #   prefix = "NDVI"
        #   inputs = (
        #       "T33..._B08",
        #       "T33..._B04",
        #   )

        first_input = first

        if "-" in first:
            possible_prefix, possible_input = first.split(
                "-",
                1,
            )

            prefix = possible_prefix
            first_input = possible_input

        parts = [
            first_input,
            *parts[1:],
        ]

        inputs = tuple(
            part
            for part in parts
            if part
        )

        return prefix, inputs

    @staticmethod
    def _get_input_identifiers(
            input_files: tuple[Path, ...],
    ) -> tuple[str, ...]:

        return tuple(
            path.stem
            for path in input_files
        )

    @staticmethod
    def _normalize_output_path(
            outfile: Path,
            task: VisualizationTask,
    ) -> Path:
        return outfile.with_name(f"{task.id}{outfile.suffix}")

    @staticmethod
    def _get_output_format(
            path: Path,
    ) -> OutputFormat:
        try:
            return OutputFormat(path.suffix.lstrip(".").lower())

        except ValueError as exc:
            raise ValueError(f"Unsupported GJTIFF output format: {path}") from exc

    @staticmethod
    def _validate_quality(
            value,
    ) -> int:

        if value is None:
            return settings.DEFAULT_PROCESSING_QUALITY

        try:
            quality = int(value)

        except (TypeError, ValueError):
            raise ValueError(f"Invalid quality: {value}")

        if not 0 <= quality <= 100:
            raise ValueError(f"Quality must be between 0 and 100, got {quality}")

        return quality

    @staticmethod
    def _validate_zoom_levels(
            value,
    ) -> list[int]:

        if value is None:
            return list(settings.DEFAULT_PROCESSING_ZOOM_LEVELS)

        if isinstance(value, str):
            value = value.split(",")

        try:
            zoom_levels = [int(level) for level in value]

        except (TypeError, ValueError):
            raise ValueError(f"Invalid zoom levels: {value}")

        if any(level < 0 for level in zoom_levels):
            raise ValueError(f"Zoom levels must be non-negative: {zoom_levels}")

        return zoom_levels

    def _get_container(self):
        client = docker.from_env()

        try:
            return client.containers.get(self._GJTIFF_CONTAINER_NAME)

        except DockerException as e:
            raise RuntimeError(
                f"GJTIFF container "
                f"'{self._GJTIFF_CONTAINER_NAME}' not found. "
                f"Error: {e}"
            ) from e

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
                stderr.decode('utf-8')
                if stderr
                else "Unknown error"
            )

            raise RuntimeError(f"GJTIFF failed with exit code {exec_result.exit_code}: {error}")

        if stdout:
            self._logger.info(f"GJTIFF output: {stdout.decode('utf-8')}")

        return stdout
