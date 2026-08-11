from pathlib import Path

import docker
from docker.errors import DockerException

from .processor import Processor
from ...domain import TileGroup, OutputFormat, ProcessorOutput
from ...settings import settings

FORMAT_FLAGS = {
    OutputFormat.JPG.value: {TileGroup.FULL_PRODUCT.value: "-J", TileGroup.WM_TILES.value: "-j"},
    OutputFormat.PNG.value: {TileGroup.FULL_PRODUCT.value: "-P", TileGroup.WM_TILES.value: "-p"},
    OutputFormat.WEBP.value: {TileGroup.FULL_PRODUCT.value: "-W", TileGroup.WM_TILES.value: "-w"},
}


class GJTIFFProcessor(Processor):
    _GJTIFF_CONTAINER_NAME = "oculus_gjtiff"

    def _process(self) -> list[ProcessorOutput]:

        quality = self._validate_int_param(
            self._job.request_properties.get("quality"),
            settings.DEFAULT_PROCESSING_QUALITY,
            "quality",
        )

        zoom_levels = self._validate_zoom_levels(
            self._job.request_properties.get("zoom_levels"),
            settings.DEFAULT_PROCESSING_ZOOM_LEVELS,
        )

        command = self._build_command(
            output_formats=self._input_files.outputs,
            input_files=self._input_files.files,
            quality=quality,
            zoom_levels=",".join(map(str, zoom_levels)),
        )

        #gjtiff_container = self._get_container()
        #self._run_command(gjtiff_container, command)  # TODO uncomment for production, delete below for testing

        print(f"Now runing gjtiff: {command}")
        import time
        time.sleep(5)

        return self._discover_outputs(wm_zoom_levels=zoom_levels)

    def _discover_outputs(self, wm_zoom_levels: list[int]) -> list[ProcessorOutput]:

        outputs: list[ProcessorOutput] = []

        processed_dir = Path(self._path_to_processed)

        if not processed_dir.exists():
            return outputs

        # map: "TCI_10m" -> full input filename
        requested_files = {
            Path(f).stem: f
            for f in self._job.requested_files
        }

        for item in processed_dir.iterdir():

            # -------------------
            # FULL outputs (files)
            # -------------------
            if item.is_file():

                try:
                    fmt = OutputFormat(item.suffix.lstrip(".").lower())
                except ValueError:
                    continue

                source_file = requested_files.get(item.stem)

                if not source_file:
                    continue

                outputs.append(
                    ProcessorOutput(
                        source_file=source_file,
                        group=TileGroup.FULL_PRODUCT,
                        format_name=fmt,
                        path=item,
                    )
                )

            # ------------------------
            # WEB_MERCATOR (dirs)
            # ------------------------
            elif item.is_dir():

                # název složky = stem input file
                source_file = requested_files.get(item.name)

                if not source_file:
                    continue

                formats = self._discover_tile_formats(item)

                for fmt in formats:
                    outputs.append(
                        ProcessorOutput(
                            source_file=source_file,
                            group=TileGroup.WM_TILES,
                            format_name=fmt,
                            path=item,
                            zoom_levels=wm_zoom_levels,
                        )
                    )

        return outputs

    @staticmethod
    def _discover_tile_formats(pyramid_root: Path) -> set[OutputFormat]:

        first_tile = next(
            (p for p in pyramid_root.rglob("*") if p.is_file()),
            None,
        )

        if first_tile is None:
            return set()

        formats = set()

        for file in first_tile.parent.iterdir():

            if not file.is_file():
                continue

            try:
                formats.add(OutputFormat(file.suffix.lstrip(".").lower()))
            except ValueError:
                pass

        return formats

    def _get_container(self) -> docker.models.containers.Container:

        client = docker.from_env()

        try:
            return client.containers.get(self._GJTIFF_CONTAINER_NAME)

        except DockerException as e:
            raise RuntimeError(f"GJTIFF container '{self._GJTIFF_CONTAINER_NAME}' not found. Error: {e}")

    def _build_command(
            self,
            output_formats: dict,
            input_files: list[Path],
            quality: int,
            zoom_levels: str
    ) -> list[str]:

        input_files = [str(file) for file in input_files]

        entered_format_flags = []

        for format_name, modes in output_formats.items():

            if format_name not in FORMAT_FLAGS:
                raise TypeError(f"Unknown format: {format_name}")

            for mode, enabled in modes.items():
                if enabled:

                    '''
                    ### GJTiff only exports into one WebMercator tiles format at a time. Defaulting to WebP.
                    
                    CESNET Slack #meta-esa-vizualizace:
                    20260318: matejkaj: Ale řekl bych, že GjTiff neumí generovat víc formátů celých produktů najednou?
                    20260318: xpulec: No neuměl, ale už jsem přidal. Platí to teda ale jen pro celkový obrázek (-W/-J/-P), ne dlaždice, tam je možné pořád generovat jen v jednom formátu.
                    '''

                    if mode == TileGroup.WM_TILES.value:
                        if format_name != OutputFormat.WEBP.value:
                            self._logger.warning(
                                f"WebMercator tiles are only supported for WEBP format. Ignoring {format_name} format.")
                        continue

                    entered_format_flags.append(FORMAT_FLAGS[format_name][mode])

        entered_format_flags.append(FORMAT_FLAGS[OutputFormat.WEBP.value][TileGroup.WM_TILES.value])

        return (
                [
                    "gjtiff",
                    "-q", str(quality),
                    "-Q",
                    "-z", zoom_levels,
                    "-o", self._path_to_processed,
                ]
                + entered_format_flags
                + input_files
        )

    def _run_command(
            self,
            container,
            command: list[str],
    ) -> None:

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

        if stdout:
            self._logger.info(stdout.decode("utf-8"))
