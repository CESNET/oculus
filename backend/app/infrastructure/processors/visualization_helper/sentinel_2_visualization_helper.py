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
        request_properties = self._job.request_properties

        requested_visualizations = request_properties.get(
            "visualizations",
            {},
        )

        outputs = self._get_outputs(
            request_properties.get("outputs", {})
        )

        tasks: list[VisualizationTask] = []

        # Single bands
        for task in self._get_single_band_tasks(
                requested_visualizations.get("bands", [])
        ):
            self._add_task_if_needed(
                tasks=tasks,
                task=task,
                outputs=outputs,
            )

        # Custom RGB composite
        rgb = requested_visualizations.get("rgb_composite")

        if rgb:
            task = self._get_rgb_task(rgb)

            if task is not None:
                self._add_task_if_needed(
                    tasks=tasks,
                    task=task,
                    outputs=outputs,
                )

        # Presets
        for preset_id in requested_visualizations.get("presets", []):
            task = self._get_preset_task(preset_id)

            if task is not None:
                self._add_task_if_needed(
                    tasks=tasks,
                    task=task,
                    outputs=outputs,
                )

        return ProcessingPlan(
            visualizations=tuple(tasks),
            outputs=outputs,
        )

    # ======================================================
    # TASK FILTERING
    # ======================================================

    def _add_task_if_needed(
            self,
            tasks: list[VisualizationTask],
            task: VisualizationTask,
            outputs: dict[OutputFormat, set[TileGroup]],
    ) -> None:

        # Do not add the same visualization twice to
        # the current processing plan.
        if any(
                existing_task.id == task.id
                for existing_task in tasks
        ):
            return

        # If all requested outputs already exist,
        # there is nothing to process.
        if self._visualization_has_outputs(
                visualization_id=task.id,
                outputs=outputs,
        ):
            self._logger.info(f"Visualization '{task.id}' already has all requested outputs. Skipping processing.")
            return

        tasks.append(task)

    def _visualization_has_outputs(
            self,
            visualization_id: str,
            outputs: dict[OutputFormat, set[TileGroup]],
    ) -> bool:

        visualization = self._feature_state.visualizations.get(visualization_id)

        if visualization is None:
            return False

        for format_name, groups in outputs.items():

            output = visualization.outputs.get(format_name)

            if output is None:
                return False

            for group in groups:

                if group == TileGroup.FULL_PRODUCT:

                    if not output.has_full_product():
                        return False

                elif group == TileGroup.WM_TILES:

                    if not output.has_wm_tiles():
                        return False

                else:
                    raise ValueError(f"Unsupported tile group: {group}")

        return True

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
                self._logger.warning(f"Unknown Sentinel-2 band: {band_name}")
                continue

            input_file = self._get_input_file(band)

            if input_file is None:
                self._logger.warning(f"Required Sentinel-2 band {band.value} was not found in feature state.")
                continue

            tasks.append(
                VisualizationTask(
                    id=band.value,
                    input_files=(input_file,),
                    prefix=None,
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
            self._logger.warning(f"Invalid Sentinel-2 RGB composite: {rgb}")
            return None

        bands = (
            red,
            green,
            blue,
        )

        input_files = self._get_input_files(bands)

        if input_files is None:
            return None

        visualization_id = f"rgb_{red.value}-{green.value}-{blue.value}"

        return VisualizationTask(
            id=visualization_id,
            input_files=input_files,
            prefix=None,
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
            self._logger.warning(f"Unknown Sentinel-2 preset: {preset_id}")
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

        visualization_id = f"rgb-{preset.id}_{'-'.join(band.value for band in bands)}"

        return VisualizationTask(
            id=visualization_id,
            input_files=input_files,
            prefix=None,
        )

    def _get_preset_index_task(
            self,
            preset: Sentinel2IndexPreset,
    ) -> VisualizationTask | None:

        bands = SENTINEL2_INDEX_BANDS[preset.index]

        input_files = self._get_input_files(bands)

        if input_files is None:
            return None

        visualization_id = f"{preset.id}_{'-'.join(band.value for band in bands)}"

        return VisualizationTask(
            id=visualization_id,
            input_files=input_files,
            prefix=preset.index.value,
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
                self._logger.warning(f"Required Sentinel-2 band {band.value} was not found in feature state.")
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
