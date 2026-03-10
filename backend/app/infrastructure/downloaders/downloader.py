import logging
from abc import ABC, abstractmethod
from typing import Optional, List

from .providers.base_provider import BaseProvider
from ...domain.job import Job
from ...settings import settings


class Downloader(ABC):
    _providers: List[BaseProvider] = []

    def __init__(self, job: Job, logger: Optional[logging.Logger] = None):
        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)

        self._job: Job = job

        self._provider: BaseProvider = self._find_provider()

    def _find_provider(self) -> BaseProvider:
        for provider in self._providers:
            if provider.has_product():
                self._logger.info(
                    f"Product {self._job.product_id} found in {provider.__class__.__name__}"
                )
                return provider

        raise ValueError(f"Product {self._job.product_id} not found in any provider")

    @abstractmethod
    def _filter_files(self, available_files: list[str]) -> list[str]:
        ...

    def download(self) -> list[str]:
        self._logger.info(f"Downloading job {self._job.id}")

        available_files: list[str] = self._provider.list_product_files()

        files_to_download: list[str] = self._filter_files(available_files=available_files)

        downloaded_files: list[str] = self._provider.download_product_files(files_to_download=files_to_download)

        self._logger.info(f"Total {len(downloaded_files)} files for job {self._job.id} downloaded")

        return downloaded_files
