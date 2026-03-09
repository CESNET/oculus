import logging
import os
from typing import Optional

from ...settings import settings
from ...domain import Job


class Processor:
    def __init__(self, job: Job, logger: Optional[logging.Logger] = None):
        self._job = job

        self._processed_data_path = os.path.join(settings.DATA_DIR, self._job.id, "data", "processed")

        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)

    def process(self) -> str:
        self._logger.info(f"Start processing for job {self._job.id}")

        os.makedirs(self._processed_data_path, exist_ok=True)

        self._processed_data_path = self._process()

        self._logger.info(f"Job ID: {self._job.id} finished processing int {self._processed_data_path}")

        return self._processed_data_path

    def _process(self) -> str:
        ...
