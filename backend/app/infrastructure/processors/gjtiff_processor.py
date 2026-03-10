import json
import os

import docker
from docker.errors import DockerException

from .processor import Processor

ZOOM_LEVELS = {
    "min_zoom": 8,
    "max_zoom": 15
}  # TODO This should probably be in the Job and changed dynamically based on the resolution of Job product...

FORMAT_OPTIONS = {
    "png": [],
    "webp": ["-w"]
}


class GJTIFFProcessor(Processor):
    def _get_container(self) -> docker.models.containers.Container:
        client = docker.from_env()

        try:
            return client.containers.get("oculus_gjtiff")
        except DockerException as e:
            raise RuntimeError(f"GJTIFF container 'oculus_gjtiff' not found. Error: {e}")

    def _build_command(self, output_format: str, input_files: list[str]) -> list[str]:
        if output_format not in FORMAT_OPTIONS:
            raise TypeError(f"Unknown output format: {output_format}")

        zoom_levels = ",".join(
            str(z) for z in range(ZOOM_LEVELS["min_zoom"], ZOOM_LEVELS["max_zoom"] + 1)
        )

        command = (
                [
                    "gjtiff",
                    "-q", "82",  # quality
                    "-Q",  # quiet mode
                    "-z", zoom_levels,  # zoom levels
                    "-o", self._path_to_processed  # output directory
                ] + FORMAT_OPTIONS[output_format]  # current format
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

        output_formats = self._job.properties.get("output_formats", ["webp"])

        for output_format in output_formats:
            command = self._build_command(output_format, input_files)

            output_files.extend(self._run_command(gjtiff_container, command))

        return output_files
