import logging
from pathlib import Path

import docker

logger = logging.getLogger(__name__)


def execute_gjtiff(input_files: list[str], output_directory: Path, zoom_levels: list[int]) -> str:
    zoom_levels = ",".join(str(zoom_level) for zoom_level in zoom_levels)
    command = ["gjtiff", "-q", "82", "-Q", "-z", zoom_levels, "-o", str(output_directory)] + input_files

    logger.info(f"Running GJTIFF: {command}")

    client = docker.from_env()
    container = client.containers.get("oculus_gjtiff")
    stdout, stderr = container.exec_run(command, stdout=True, stderr=True, tty=False, demux=True).output

    if stderr:
        logger.error(stderr.decode("utf-8"))

    return stdout.decode("utf-8")
