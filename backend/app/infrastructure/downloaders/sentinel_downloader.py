from abc import abstractmethod

from . import Downloader
from .providers import GSSProvider, CDSEProvider
from ...domain import Job


class SentinelDownloader(Downloader):
    def __init__(self, job: Job, logger=None):
        self._providers = [
            GSSProvider(job=job),
            CDSEProvider(job=job)
        ]

        super().__init__(job, logger)

    @abstractmethod
    def _filter_files(self, available_files: list[str]) -> list[str]:
        ...
