import logging
import os
from abc import ABC, abstractmethod

from ....domain import Job
from ....settings import settings


class BaseProvider(ABC):
    def __init__(
            self,
            job: Job,
            logger: logging.Logger | None = None
    ):
        self._logger = logger or logging.getLogger(settings.APP_NAME)

        self._job = job

        self._path_to_downloaded: str = os.path.join(self._job.data_directory, "downloaded")

    @abstractmethod
    def has_product(self) -> bool:
        ...

    @abstractmethod
    def list_product_files(self) -> list[str]:
        ...

    @abstractmethod
    def download_product_files(self, files_to_download: list[str]) -> list[str]:
        ...

    def download_entire_product(self) -> list[str]:
        files_to_download: list[str] = self.list_product_files()
        downloaded_files: list[str] = self.download_product_files(files_to_download=files_to_download)
        return downloaded_files
