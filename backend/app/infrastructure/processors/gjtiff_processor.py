import json

import docker
from docker.errors import DockerException

from .processor import Processor
from ...settings import settings

FORMAT_FLAGS = {
    "jpg": {"product": "-J", "tiles": "-j"},
    "png": {"product": "-P", "tiles": "-p"},
    "webp": {"product": "-W", "tiles": "-w"},
}
# TODO tiles jdou generovat jen v jednom formátu, asi chceme upřednosťnovat gjtiff, tak to nějak ošetřit při skládání commandu


class GJTIFFProcessor(Processor):
    _GJTIFF_CONTAINER_NAME: str = "oculus_gjtiff"

    def _process(self) -> list[str]:
        quality = self._validate_int_param(
            self._job.properties.get("quality"),
            settings.DEFAULT_PROCESSING_QUALITY,
            "quality"
        )

        zoom_levels = self._validate_zoom_levels(
            self._job.properties.get("zoom_levels"),
            settings.DEFAULT_PROCESSING_ZOOM_LEVELS
        )
        zoom_levels_str = ",".join(map(str, zoom_levels))

        output_formats = self._job.properties.get(
            "outputs",
            settings.DEFAULT_PROCESSING_OUTPUT_FORMATS  # default fallback
        )

        command = self._build_command(output_formats, self._input_files, quality, zoom_levels_str)
        gjtiff_container = self._get_container()

        return self._run_command(gjtiff_container, command)

    def _get_container(self) -> docker.models.containers.Container:
        client = docker.from_env()
        try:
            return client.containers.get(self._GJTIFF_CONTAINER_NAME)
        except DockerException as e:
            raise RuntimeError(f"GJTIFF container '{self._GJTIFF_CONTAINER_NAME}' not found. Error: {e}")

    def _build_command(self, outputs: dict, input_files: list[str], quality: int, zoom_levels: str) -> list[str]:
        entered_format_flags = []

        for format, modes in outputs.items():
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
        self._logger.debug(output_str)

        try:
            gjtiff_output = json.loads(output_str)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse GJTIFF JSON output: {e}")

        # TODO tady jinak pracovat s outfiles. A nevím, jestli to teda vlastně nakonec potřebujeme..? Jestli není jednodušší předpokládat, že prostě v processed jsou soubory jen podle return code gjtiffu?

        return [item["outfile"] for item in gjtiff_output if "outfile" in item]
