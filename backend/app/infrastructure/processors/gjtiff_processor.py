import json
import os

import docker
from docker.errors import DockerException

from .processor import Processor

ZOOM_LEVELS: dict[str, int] = {
    "min_zoom": 8,
    "max_zoom": 15
}  # TODO This should probably be in the Job and changed dynamically based on the resolution of Job product...

FORMAT_FLAGS = {
    "jpg": {"product": "-J", "tiles": "-j"},
    "png": {"product": "-P", "tiles": "-p"},
    "webp": {"product": "-W", "tiles": "-w"},
}


class GJTIFFProcessor(Processor):
    def _get_container(self) -> docker.models.containers.Container:
        client = docker.from_env()

        try:
            return client.containers.get("oculus_gjtiff")
        except DockerException as e:
            raise RuntimeError(f"GJTIFF container 'oculus_gjtiff' not found. Error: {e}")

    def _build_command(self, outputs: dict, input_files: list[str], zoom_levels=None) -> list[str]:
        if zoom_levels is None:
            zoom_levels = ZOOM_LEVELS

        zoom_levels = ",".join(
            str(z) for z in range(zoom_levels["min_zoom"], zoom_levels["max_zoom"] + 1)
        )

        flags = []

        for format, modes in outputs.items():
            if format not in FORMAT_FLAGS:
                raise TypeError(f"Unknown format: {format}")

            for mode, enabled in modes.items():
                if enabled:
                    flags.append(FORMAT_FLAGS[format][mode])

        command = (
                [
                    "gjtiff",
                    "-q", "82",  # Quality
                    "-Q",  # Quiet
                    "-z", zoom_levels,  # WebMercator zoom levels
                    "-o", self._path_to_processed  # Output path, processed files will be stored in this directory
                ]
                + flags
                + input_files
        )

        return command

    def _run_command(self, container: docker.models.containers.Container, command: list[str]) -> list[str]:
        self._logger.info(f"Running GJTIFF command: {' '.join(command)}")

        try:
            exec_result = container.exec_run(
                cmd=command,
                stdout=True,
                stderr=True,
                tty=False,
                demux=True
            )
        except DockerException as e:
            raise RuntimeError(f"GJTIFF container execution failed. Error: {e}")

        stdout, stderr = exec_result.output

        if stderr:
            raise RuntimeError(f"GJTIFF failed! Error: {stderr.decode('utf-8')}")

        output_str = stdout.decode("utf-8")
        self._logger.debug(output_str)

        try:
            gjtiff_output = json.loads(output_str)

        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse GJTIFF JSON output: {e}")

        return [item["outfile"] for item in gjtiff_output if "outfile" in item]

    def _process(self) -> list[str]:
        input_files = self._job.downloaded_files
        if not input_files:
            raise ValueError("No input files specified!")

        os.makedirs(self._path_to_processed, exist_ok=True)

        output_files: list[str] = []

        gjtiff_container = self._get_container()

        outputs = self._job.properties.get(
            "outputs",
            {"webp": {"product": True, "tiles": True}}  # default fallback
        )

        command = self._build_command(outputs, input_files)
        output_files.extend(self._run_command(gjtiff_container, command))

        return output_files
