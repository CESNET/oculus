from .visualization_helper import VisualizationHelper
from .landsat_visualization_helper import LandsatVisualizationHelper
from .sentinel_1_visualization_helper import Sentinel1VisualizationHelper
from .sentinel_2_visualization_helper import Sentinel2VisualizationHelper
from ....domain import Job, JobDataset, FeatureState


class VisualizationHelperFactory:
    _VISUALIZATION_HELPER_MAP = {
        JobDataset.SENTINEL1: Sentinel1VisualizationHelper,
        JobDataset.SENTINEL2: Sentinel2VisualizationHelper,
        JobDataset.LANDSAT: LandsatVisualizationHelper,
    }

    def _resolve_visualization_helper(self, entry, job):
        if isinstance(entry, type):
            return entry

        elif isinstance(entry, dict):
            selector = entry.get("selector")
            mapping = entry.get("map")

            if not selector or not mapping:
                raise ValueError("Invalid dict in visualization helper map")

            key = selector(job)
            next_entry = mapping.get(key)

            if next_entry is None:
                raise ValueError(f"Unsupported key {key}")

            return self._resolve_visualization_helper(next_entry, job)

        else:
            raise TypeError(f"Invalid entry type: {type(entry)}")

    def get_visualization_helper(self, job: Job, feature_state: FeatureState, logger=None) -> VisualizationHelper:
        dataset_entry = self._VISUALIZATION_HELPER_MAP.get(job.dataset)

        if dataset_entry is None:
            raise ValueError(f"Unsupported dataset: {job.dataset}")

        cls = self._resolve_visualization_helper(dataset_entry, job)

        return cls(job, feature_state, logger)


visualization_helper_factory = VisualizationHelperFactory()
