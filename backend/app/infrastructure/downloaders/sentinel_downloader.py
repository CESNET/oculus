from . import Downloader
from .providers import GSSProvider, CDSEProvider
from ...domain import Job


class SentinelDownloader(Downloader):
    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

        self._providers = [
            GSSProvider(job=job),
            CDSEProvider(job=job)
        ]
