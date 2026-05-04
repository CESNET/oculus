import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List

from .providers import BaseProvider
from ...domain import Job, FeatureState
from ...settings import settings


class DownloadService(ABC):
    _providers: List[BaseProvider] = []

    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger: Optional[logging.Logger] = None
    ):
        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)

        self._job: Job = job
        self._feature_state: FeatureState = feature_state

        self._provider: BaseProvider = self._find_provider()

    def _find_provider(self) -> BaseProvider:
        for provider in self._providers:
            if provider.has_product():
                self._logger.info(
                    f"Product {self._job.feature_id} found in {provider.__class__.__name__}"
                )
                return provider

        raise ValueError(f"Product {self._job.feature_id} not found in any provider")

    @staticmethod
    def _extract_filename(path: str) -> str:
        return Path(path).name

    def filter_files(
            self,
            available_files: list[str],
            already_downloaded: set[str],
    ) -> list[str]:
        available_files = self._filter_files(available_files)

        available_map = {
            self._extract_filename(f): f
            for f in available_files
        }

        already_downloaded_names = {
            self._extract_filename(p) for p in already_downloaded
        }

        return [
            original_path
            for name, original_path in available_map.items()
            if name not in already_downloaded_names
        ]

    @abstractmethod
    def _filter_files(self, available_files: list[str]) -> list[str]:
        ...

    def download(self, already_downloaded: set[str]) -> list[str]:
        self._logger.info(f"Downloading job {self._job.id}")

        available_files: list[str] = self._provider.list_product_files()

        files_to_download: list[str] = self.filter_files(
            available_files=available_files,
            already_downloaded=already_downloaded,
        )

        start = time.perf_counter()

        downloaded_files: list[str] = self._provider.download_product_files(
            files_to_download=files_to_download
        )

        end = time.perf_counter()

        self._logger.info(
            f"Downloaded {len(downloaded_files)} files in {(end - start):.3f}s"
        )

        return downloaded_files
