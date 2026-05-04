from .landsat_download_service import LandsatDownloadService
from .sentinel_1_download_service import Sentinel1DownloadService
from .sentinel_2_download_service import Sentinel2DownloadService
from ...domain import Job, JobDataset, FeatureState


class DownloadServiceFactory:
    _DOWNLOAD_SERVICE_MAP = {
        JobDataset.SENTINEL1: Sentinel1DownloadService,
        JobDataset.SENTINEL2: Sentinel2DownloadService,
        JobDataset.LANDSAT: LandsatDownloadService,
    }

    def _resolve_download_service(self, entry, job):
        if isinstance(entry, type):
            return entry

        elif isinstance(entry, dict):
            selector = entry.get("selector")
            mapping = entry.get("map")

            if not selector or not mapping:
                raise ValueError("Invalid dict in downloader map")

            key = selector(job)
            next_entry = mapping.get(key)

            if next_entry is None:
                raise ValueError(f"Unsupported key {key}")

            return self._resolve_download_service(next_entry, job)

        else:
            raise TypeError(f"Invalid entry type: {type(entry)}")

    def get_download_service(self, job: Job, feature_state: FeatureState, logger=None):
        dataset_entry = self._DOWNLOAD_SERVICE_MAP.get(job.dataset)

        if dataset_entry is None:
            raise ValueError(f"Unsupported dataset: {job.dataset}")

        cls = self._resolve_download_service(dataset_entry, job)

        return cls(job, feature_state, logger)


download_service_factory = DownloadServiceFactory()
