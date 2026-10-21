from pathlib import Path

from .processing_plan import (
    ProcessingPlan,
    VisualizationTask,
)
from .visualization_helper import VisualizationHelper
from ....domain import (
    OutputFormat,
    Sentinel1Polarization,
    TileGroup,
)


class Sentinel1VisualizationHelper(VisualizationHelper):

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

        # Polarizations
        for task in self._get_polarization_tasks(
                requested_visualizations.get("polarizations", [])
        ):
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

    # ======================================================
    # POLARIZATIONS
    # ======================================================

    def _get_polarization_tasks(
            self,
            polarizations: list[str],
    ) -> list[VisualizationTask]:

        tasks: list[VisualizationTask] = []

        for polarization in polarizations:

            try:
                polarization = Sentinel1Polarization(polarization)

            except ValueError:
                self._logger.warning(f"Unknown Sentinel-1 polarization: {polarization}")
                continue

            input_file = self._get_input_file(polarization)

            if input_file is None:
                self._logger.warning(
                    f"Required Sentinel-1 polarization {polarization.value} was not found in feature state.")
                continue

            tasks.append(
                VisualizationTask(
                    id=polarization.value,
                    input_files=(input_file,),
                    prefix=None,
                )
            )

        return tasks

    # ======================================================
    # INPUT FILES
    # ======================================================

    def _get_input_files(
            self,
            polarizations: tuple[Sentinel1Polarization, ...],
    ) -> tuple[Path, ...] | None:

        input_files: list[Path] = []

        for polarization in polarizations:

            input_file = self._get_input_file(polarization)

            if input_file is None:
                self._logger.warning(
                    f"Required Sentinel-1 polarization {polarization.value} was not found in feature state.")
                return None

            input_files.append(input_file)

        return tuple(input_files)

    def _get_input_file(
            self,
            polarization: Sentinel1Polarization,
    ) -> Path | None:

        for file_state in self._feature_state.input_files.values():

            if file_state.download_path is None:
                continue

            if self._file_contains_polarization(
                    file_state.filename,
                    polarization,
            ):
                return file_state.download_path

        return None

    @staticmethod
    def _file_contains_polarization(
            filename: str,
            polarization: Sentinel1Polarization,
    ) -> bool:

        filename = Path(filename).name.lower()

        parts = filename.split("-")

        return polarization.value.lower() in parts
