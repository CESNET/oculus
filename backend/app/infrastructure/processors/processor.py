import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

from ...domain import Job
from ...settings import settings


class Processor(ABC):
    def __init__(self, job: Job, logger: Optional[logging.Logger] = None):
        self._job = job

        self._path_to_processed = os.path.join(settings.DATA_DIR, self._job.id, "data", "processed")

        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)

    def process(self) -> list[str]:
        self._logger.info(f"Processing job {self._job.id}")

        processed_files: list[str] = self._process()

        return processed_files

    @abstractmethod
    def _process(self) -> list[str]:
        ...
