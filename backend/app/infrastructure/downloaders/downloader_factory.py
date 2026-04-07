from .landsat_downloader import LandsatDownloader
from .sentinel_1_downloader import Sentinel1Downloader
from .sentinel_2_downloader import Sentinel2Downloader
from ...domain import JobDataset


class DownloaderFactory:
    ###
    # Puvodni z job.properties["platform"]
    ###
    # _DOWNLOADER_MAP = {
    #     JobDataset.LANDSAT: LandsatDownloader,
    #     JobDataset.SENTINEL: {
    #         "selector": lambda job: job.properties["platform"],
    #         "map": {
    #             "SENTINEL-1": Sentinel1Downloader,
    #             "SENTINEL-2": Sentinel2Downloader,
    #         }
    #     }
    # }

    _DOWNLOADER_MAP = {
        JobDataset.SENTINEL1: Sentinel1Downloader,
        JobDataset.SENTINEL2: Sentinel2Downloader,
        JobDataset.LANDSAT: LandsatDownloader,
    }

    def _resolve_downloader(self, entry, job):
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

            return self._resolve_downloader(next_entry, job)

        else:
            raise TypeError(f"Invalid entry type: {type(entry)}")

    def get_downloader(self, job, logger=None):
        #dataset_entry = self._DOWNLOADER_MAP.get(job.dataset.family) # Puvodni z job.properties["platform"]
        dataset_entry = self._DOWNLOADER_MAP.get(job.dataset)

        if dataset_entry is None:
            raise ValueError(f"Unsupported dataset: {job.dataset}")

        cls = self._resolve_downloader(dataset_entry, job)

        return cls(job, logger)


downloader_factory = DownloaderFactory()
