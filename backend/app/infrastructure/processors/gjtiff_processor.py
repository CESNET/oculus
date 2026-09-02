from pathlib import Path

import docker
from docker.errors import DockerException

from .processor import Processor
from .visualization_helper import ProcessingPlan
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

        self._logger.info(f"GJTIFF command: {' '.join(command)}")

        """
        container = self._get_container()

        self._run_command(
            container=container,
            command=command,
        )
        """  # Todo uncomment for production

        import time
        time.sleep(5)

        return self._discover_outputs(
            processing_plan=processing_plan,
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

            visualization_inputs.append(
                f"{task.id.upper()}@{input_files}"
            )

        format_flags = self._build_format_flags(
            processing_plan.outputs,
        )

        processed_directory = (
                self._feature_state.feature_root_directory
                / "processed"
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
    def _build_format_flags(
            outputs: dict[OutputFormat, set[TileGroup]],
    ) -> list[str]:

        flags: list[str] = []

        for format_name, groups in outputs.items():

            if format_name not in FORMAT_FLAGS:
                raise ValueError(
                    f"Unsupported output format: {format_name}"
                )

            for group in groups:

                flag = FORMAT_FLAGS[format_name].get(group)

                if flag is None:
                    raise ValueError(
                        f"Unsupported output combination: "
                        f"{format_name}/{group}"
                    )

                flags.append(flag)

        return flags

    @staticmethod
    def _validate_quality(
            value,
    ) -> int:

        if value is None:
            return settings.DEFAULT_PROCESSING_QUALITY

        try:
            quality = int(value)
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid quality: {value}"
            )

        if not 0 <= quality <= 100:
            raise ValueError(
                f"Quality must be between 0 and 100, got {quality}"
            )

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
        except (TypeError, ValueError):
            raise ValueError(
                f"Invalid zoom levels: {value}"
            )

        if any(level < 0 for level in zoom_levels):
            raise ValueError(
                f"Zoom levels must be non-negative: {zoom_levels}"
            )

        return zoom_levels

    def _discover_outputs(
            self,
            processing_plan: ProcessingPlan,
            zoom_levels: list[int],
    ) -> list[ProcessorOutput]:

        processed_directory = (
                self._feature_state.feature_root_directory
                / "processed"
        )

        if not processed_directory.exists():
            return []

        visualization_ids = {
            task.id
            for task in processing_plan.visualizations
        }

        outputs: list[ProcessorOutput] = []

        for item in processed_directory.iterdir():

            if item.is_file():

                visualization_id = item.stem

                if visualization_id not in visualization_ids:
                    continue

                try:
                    format_name = OutputFormat(
                        item.suffix.lstrip(".").lower()
                    )
                except ValueError:
                    continue

                outputs.append(
                    ProcessorOutput(
                        visualization_id=visualization_id,
                        group=TileGroup.FULL_PRODUCT,
                        format_name=format_name,
                        path=item,
                    )
                )

            elif item.is_dir():

                visualization_id = item.name

                if visualization_id not in visualization_ids:
                    continue

                formats = self._discover_tile_formats(
                    item
                )

                for format_name in formats:
                    outputs.append(
                        ProcessorOutput(
                            visualization_id=visualization_id,
                            group=TileGroup.WM_TILES,
                            format_name=format_name,
                            path=item,
                            zoom_levels=zoom_levels,
                        )
                    )

        return outputs

    @staticmethod
    def _discover_tile_formats(
            pyramid_root: Path,
    ) -> set[OutputFormat]:

        first_tile = next(
            (
                path
                for path in pyramid_root.rglob("*")
                if path.is_file()
            ),
            None,
        )

        if first_tile is None:
            return set()

        formats: set[OutputFormat] = set()

        for file in first_tile.parent.iterdir():

            if not file.is_file():
                continue

            try:
                formats.add(
                    OutputFormat(
                        file.suffix.lstrip(".").lower()
                    )
                )
            except ValueError:
                continue

        return formats

    def _get_container(self):
        client = docker.from_env()

        try:
            return client.containers.get(
                self._GJTIFF_CONTAINER_NAME
            )

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
    ) -> None:

        self._logger.info(
            f"Running GJTIFF command: {' '.join(command)}"
        )

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

            raise RuntimeError(
                "GJTIFF failed with exit code "
                f"{exec_result.exit_code}: {error}"
            )

        if stdout:
            self._logger.info(
                stdout.decode("utf-8")
            )
