from . import Downloader
from .providers import USGSProvider
from ...domain import Job


class LandsatDownloader(Downloader):
    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

        self._providers = [
            USGSProvider(job=job)
        ]
