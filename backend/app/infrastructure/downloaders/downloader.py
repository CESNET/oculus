import logging
import os
from abc import ABC, abstractmethod

from ...config import APP_NAME, DATA_DIR
from ...domain import Job


class Downloader(ABC):
    def __init__(self, job: Job, logger: logging.Logger | None = None):
        self._job: Job = job

        self._downloaded_data_path = os.path.join(DATA_DIR, self._job.id, "data", "downloaded")

        self._logger: logging.Logger = logger or logging.getLogger(APP_NAME)

    def download(self) -> str:
        self._logger.info(f"Starting download for job ID: {self._job.id}")

        os.makedirs(self._downloaded_data_path, exist_ok=True)

        self._downloaded_data_path = self._download()

        self._logger.info(f"Job ID: {self._job.id} finished downloading int {self._downloaded_data_path}")

        return self._downloaded_data_path

    @abstractmethod
    def _download(self) -> str:
        pass
