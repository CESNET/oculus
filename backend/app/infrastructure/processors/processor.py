import logging
import os
from typing import Optional

from ...config import APP_NAME, DATA_DIR


class Processor:
    _processed_data_path: str

    def __init__(self, job_id: str, logger: Optional[logging.Logger] = None):
        self._job_id = job_id

        self._logger: logging.Logger = logger or logging.getLogger(APP_NAME)

    def process(self) -> str:
        self._logger.info(f"Start processing for job {self._job_id}")

        self._processed_data_path = os.path.join(DATA_DIR, self._job_id, "data", "processed")
        os.makedirs(self._processed_data_path, exist_ok=True)

        return self._process()

    def _process(self) -> str:
        ...


