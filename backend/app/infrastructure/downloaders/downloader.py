import logging
import os
from typing import Optional

from ...config import APP_NAME, DATA_DIR


class Downloader:
    _downloaded_data_path: str

    def __init__(self, job_id: str, logger: Optional[logging.Logger] = None):
        self._job_id = job_id

        self._logger: logging.Logger = logger or logging.getLogger(APP_NAME)

    def download(self) -> str:
        self._logger.info(f"Start download for job {self._job_id}")

        self._downloaded_data_path = os.path.join(DATA_DIR, self._job_id, "data", "downloaded")
        os.makedirs(self._downloaded_data_path, exist_ok=True)

        return self._download()

    def _download(self) -> str:
        ...
