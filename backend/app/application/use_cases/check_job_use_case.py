import logging
from typing import Optional

from .use_case import UseCase
from ...domain import Job, JobRepository, FAILED_STATUSES


class CheckJobUseCase(UseCase):
    def __init__(
            self,
            repository: JobRepository,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(repository, logger)

    def execute(self, job_id: Optional[str]) -> str:
        if not job_id:
            raise ValueError("Job ID is required")

        job: Job = self._repository.get(job_id)

        if job.status in FAILED_STATUSES:
            raise RuntimeError(f"Job {job_id} failed. Status: {job.status}. Error: {job.fail_reason}")

        return job_id
