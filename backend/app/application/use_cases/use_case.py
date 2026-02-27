import logging
from typing import Optional

from ...config import APP_NAME
from ...domain.job_repository import JobRepository


class UseCase:
    def __init__(self, repository: JobRepository, logger: Optional[logging.Logger] = None):
        self._repository = repository
        self._logger = logger or logging.getLogger(APP_NAME)

    def execute(self, job_id: Optional[str]) -> str:
        raise NotImplementedError(f"Subclasses of {self.__class__.__name__} must implement execute(job_id)")
