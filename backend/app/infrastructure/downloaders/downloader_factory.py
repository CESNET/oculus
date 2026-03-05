import logging
from typing import Optional

from .landsat_downloader import LandsatDownloader
from .sentinel_downloader import SentinelDownloader
from ...domain import Job, JobDataset


class DownloaderFactory:
    _DOWNLOADER_MAP = {
        JobDataset.LANDSAT: LandsatDownloader,
        JobDataset.SENTINEL: SentinelDownloader,
    }

    def get_downloader(self, job: Job, logger: Optional[logging.Logger] = None):
        cls = self._DOWNLOADER_MAP.get(job.dataset, None)
        if cls is None:
            raise ValueError(f"Unsupported dataset: {job.dataset}")

        return cls(job, logger)


downloader_factory = DownloaderFactory()
