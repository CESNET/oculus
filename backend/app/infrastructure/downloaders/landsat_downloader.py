from . import Downloader
from .providers import USGSProvider
from ...domain import Job


class LandsatDownloader(Downloader):
    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

        self._providers = [
            USGSProvider(job=job)
        ]

    def _filter_files(self, available_files: list[str]) -> list[str]:
        raise NotImplementedError("Files filtering is not implemented for Landsat!")