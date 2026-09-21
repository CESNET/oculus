import logging
from abc import ABC, abstractmethod

from .processing_plan import (
    ProcessingPlan,
)
from ....domain import (
    FeatureState,
    Job,
    OutputFormat,
    TileGroup,
)
from ....settings import settings


class VisualizationHelper(ABC):

    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger=None,
    ):
        self._job: Job = job
        self._feature_state: FeatureState = feature_state
        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)

    def create_processing_plan(self) -> ProcessingPlan:
        return self._create_processing_plan()

    @abstractmethod
    def _create_processing_plan(self) -> ProcessingPlan:
        ...

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
