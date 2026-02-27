# app/application/use_cases/cleanup_use_case.py
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from .use_case import UseCase
from ...domain.job import Job
from ...domain.job_repository import JobRepository
from ...config import DATA_DIR  # složky s daty jobů

class CleanupJobUseCase(UseCase):
    """
    Use-case pro čištění starých jobů.
    Stateles – container předává repository a logger.
    """
    def __init__(self, repository: JobRepository, logger: Optional[logging.Logger] = None):
        super().__init__(repository=repository, logger=logger)

    def execute(self, job_id: Optional[str]) -> int:
        threshold = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
        expired_jobs: list[Job] = self._repository.find_expired(threshold)
        deleted_count = 0

        for job in expired_jobs:
            job_id = job.id

            # TODO tady bude mazání

            self._repository.delete(job_id)
            self._logger.debug(f"Job {job_id} deleted from repository")
            deleted_count += 1

        self._logger.info(f"Cleanup complete. {deleted_count} jobs deleted.")

        return deleted_count