from pathlib import Path

from .processing_plan import (
    ProcessingPlan,
    VisualizationTask,
)
from .visualization_helper import VisualizationHelper
from ....domain import (
    OutputFormat,
    SENTINEL2_INDEX_BANDS,
    SENTINEL2_PRESETS,
    Sentinel2Band,
    Sentinel2IndexPreset,
    Sentinel2RGBPreset,
    TileGroup,
)


class Sentinel2VisualizationHelper(VisualizationHelper):

    def _create_processing_plan(self) -> ProcessingPlan:
        properties = self._job.request_properties

        visualizations = properties.get(
            "visualizations",
            {},
        )

        tasks: list[VisualizationTask] = []

        # Single bands
        tasks.extend(
            self._get_single_band_tasks(
                visualizations.get("bands", [])
            )
        )

        # Custom RGB composite
        rgb = visualizations.get("rgb_composite")

        if rgb:
            task = self._get_rgb_task(rgb)

            if task is not None:
                tasks.append(task)

        # Presets
        for preset_id in visualizations.get("presets", []):
            task = self._get_preset_task(preset_id)

            if task is not None:
                tasks.append(task)

        return ProcessingPlan(
            visualizations=tuple(tasks),
            outputs=self._get_outputs(
                properties.get("outputs", {})
            ),
        )

    # ======================================================
    # OUTPUTS
    # ======================================================

    @staticmethod
    def _get_outputs(
            outputs: dict,
    ) -> dict[OutputFormat, set[TileGroup]]:
        result: dict[OutputFormat, set[TileGroup]] = {}

        for format_name, groups in outputs.items():
            try:
                output_format = OutputFormat(format_name)
            except ValueError:
                continue

            tile_groups: set[TileGroup] = set()

            if groups.get("full_product", False):
                tile_groups.add(TileGroup.FULL_PRODUCT)

            if groups.get("wm_tiles", False):
                tile_groups.add(TileGroup.WM_TILES)

            if tile_groups:
                result[output_format] = tile_groups

        return result

    # ======================================================
    # SINGLE BANDS
    # ======================================================

    def _get_single_band_tasks(
            self,
            bands: list[str],
    ) -> list[VisualizationTask]:
        tasks: list[VisualizationTask] = []

        for band_name in bands:
            try:
                band = Sentinel2Band(band_name)
            except ValueError:
                self._logger.warning(
                    f"Unknown Sentinel-2 band: {band_name}"
                )
                continue

            input_file = self._get_input_file(band)

            if input_file is None:
                self._logger.warning(
                    f"Required Sentinel-2 band {band.value} "
                    f"was not found in feature state."
                )
                continue

            tasks.append(
                VisualizationTask(
                    id=band.value,
                    input_files=(input_file,),
                    prefix=False
                )
            )

        return tasks

    # ======================================================
    # CUSTOM RGB
    # ======================================================

    def _get_rgb_task(
            self,
            rgb: dict,
    ) -> VisualizationTask | None:
        try:
            red = Sentinel2Band(rgb["red"])
            green = Sentinel2Band(rgb["green"])
            blue = Sentinel2Band(rgb["blue"])

        except (KeyError, ValueError):
            self._logger.warning(
                f"Invalid Sentinel-2 RGB composite: {rgb}"
            )
            return None

        bands = (red, green, blue)

        input_files = self._get_input_files(bands)

        if input_files is None:
            return None

        visualization_id = (
            f"rgb:{red.value}:{green.value}:{blue.value}"
        )

        return VisualizationTask(
            id=visualization_id,
            input_files=input_files,
            prefix=False
        )

    # ======================================================
    # PRESETS
    # ======================================================

    def _get_preset_task(
            self,
            preset_id: str,
    ) -> VisualizationTask | None:
        preset = SENTINEL2_PRESETS.get(preset_id)

        if preset is None:
            self._logger.warning(
                f"Unknown Sentinel-2 preset: {preset_id}"
            )
            return None

        if isinstance(preset, Sentinel2RGBPreset):
            return self._get_preset_rgb_task(preset)

        if isinstance(preset, Sentinel2IndexPreset):
            return self._get_preset_index_task(preset)

        return None

    def _get_preset_rgb_task(
            self,
            preset: Sentinel2RGBPreset,
    ) -> VisualizationTask | None:
        bands = (
            preset.composite.red,
            preset.composite.green,
            preset.composite.blue,
        )

        input_files = self._get_input_files(bands)

        if input_files is None:
            return None

        return VisualizationTask(
            id=preset.id,
            input_files=input_files,
            prefix=False
        )

    def _get_preset_index_task(
            self,
            preset: Sentinel2IndexPreset,
    ) -> VisualizationTask | None:
        bands = SENTINEL2_INDEX_BANDS[preset.index]

        input_files = self._get_input_files(bands)

        if input_files is None:
            return None

        return VisualizationTask(
            id=preset.id,
            input_files=input_files,
            prefix=True
        )

    # ======================================================
    # INPUT FILES
    # ======================================================

    def _get_input_files(
            self,
            bands: tuple[Sentinel2Band, ...],
    ) -> tuple[Path, ...] | None:
        input_files: list[Path] = []

        for band in bands:
            input_file = self._get_input_file(band)

            if input_file is None:
                self._logger.warning(
                    f"Required Sentinel-2 band {band.value} "
                    f"was not found in feature state."
                )
                return None

            input_files.append(input_file)

        return tuple(input_files)

    def _get_input_file(
            self,
            band: Sentinel2Band,
    ) -> Path | None:
        for file_state in self._feature_state.input_files.values():
            if file_state.download_path is None:
                continue

            if self._file_contains_band(
                    file_state.filename,
                    band,
            ):
                return file_state.download_path

        return None

    @staticmethod
    def _file_contains_band(
            filename: str,
            band: Sentinel2Band,
    ) -> bool:
        filename = Path(filename).name

        parts = filename.replace(".", "_").split("_")

        return band.value in parts
