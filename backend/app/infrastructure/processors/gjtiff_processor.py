import json
from pathlib import Path

import docker
from docker.errors import DockerException

from .processor import Processor
from ...settings import settings

FORMAT_FLAGS = {
    "jpg": {"product": "-J", "tiles": "-j"},
    "png": {"product": "-P", "tiles": "-p"},
    "webp": {"product": "-W", "tiles": "-w"},
}


class GJTIFFProcessor(Processor):
    _GJTIFF_CONTAINER_NAME: str = "oculus_gjtiff"

    def _process(self) -> list[str]:

        quality = self._validate_int_param(
            self._job.request_properties.get("quality"),
            settings.DEFAULT_PROCESSING_QUALITY,
            "quality"
        )

        zoom_levels = self._validate_zoom_levels(
            self._job.request_properties.get("zoom_levels"),
            settings.DEFAULT_PROCESSING_ZOOM_LEVELS
        )

        zoom_levels_str = ",".join(map(str, zoom_levels))

        output_formats = (
            self._job.request_properties.get(
                "outputs",
                settings.DEFAULT_PROCESSING_OUTPUT_FORMATS
            )
        )

        command = self._build_command(
            output_formats,
            self._input_files,
            quality,
            zoom_levels_str
        )

        """
        gjtiff_container = self._get_container()

        outfiles_without_ext =  self._run_command(
            gjtiff_container,
            command
        )
        """

        # DEBUG only vvv, for production uncomment above for executing gjtiff ^^^
        import time
        time.sleep(3)
        outfiles_without_ext = ["/data/oculus/2206d810-dacf-4017-8d74-56bbd9d070f1/data/processed/T39RWJ_20260503T070731_TCI_10m.jpg"]

        return outfiles_without_ext

    def _get_container(
            self
    ) -> docker.models.containers.Container:

        client = docker.from_env()

        try:

            return client.containers.get(
                self._GJTIFF_CONTAINER_NAME
            )

        except DockerException as e:
            raise RuntimeError(f"GJTIFF container '{self._GJTIFF_CONTAINER_NAME}' not found. Error: {e}")

    def _build_command(
            self,
            output_formats: dict,
            input_files: list[str],
            quality: int,
            zoom_levels: str
    ) -> list[str]:

        entered_format_flags = []

        for format, modes in output_formats.items():
            if format not in FORMAT_FLAGS:
                raise TypeError(f"Unknown format: {format}")

            for mode, enabled in modes.items():
                if enabled:
                    entered_format_flags.append(FORMAT_FLAGS[format][mode])

        command = (
                [
                    "gjtiff",
                    "-q", str(quality),  # Output image quality
                    "-Q",  # Quiet
                    "-z", zoom_levels,  # WebMercator zoom levels
                    "-o", self._path_to_processed  # Output path, processed files will be stored in this directory
                ]
                + entered_format_flags
                + input_files
        )

        return command

    def _run_command(self, container, command: list[str]) -> list[str]:
        self._logger.info(f"Running GJTIFF command: {' '.join(command)}")

        exec_result = container.exec_run(cmd=command, stdout=True, stderr=True, tty=False, demux=True)
        stdout, stderr = exec_result.output

        if stderr:
            raise RuntimeError(f"GJTIFF failed! Error: {stderr.decode('utf-8')}")

        output_str = stdout.decode("utf-8")

        self._logger.info(output_str)

        try:
            gjtiff_output = json.loads(output_str)

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse GJTIFF JSON output: {e}")

        # TODO tady jinak pracovat s outfiles. A nevím, jestli to teda vlastně nakonec potřebujeme..? Jestli není jednodušší předpokládat, že prostě v processed jsou soubory jen podle return code gjtiffu?

        outfiles = [item["outfile"] for item in gjtiff_output if "outfile" in item]
        outfiles_without_ext = [
            str(Path(item["outfile"]).with_suffix('')) for item in gjtiff_output if "outfile" in item
        ]

        return outfiles_without_ext
