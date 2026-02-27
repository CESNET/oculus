import logging
from typing import Optional

from .use_case import UseCase
from ...domain.job import Job
from ...domain.job_repository import JobRepository


class FinalizeJobUseCase(UseCase):
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

        job.mark_finalizing()
        self._repository.save(job)

        self._logger.info(f"Finalizing job {job.id}")
        # TODO: tady bude něco jako vracení requestu zpět frontendu

        job.mark_finished()
        self._repository.save(job)

        self._logger.info(f"Job {job.id} finished")
        return job.id
