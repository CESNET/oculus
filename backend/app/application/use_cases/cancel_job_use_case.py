import logging
from typing import Optional

from .use_case import UseCase
from ...domain import Job, JobRepository, JobStatus, FAILED_STATUSES
from ...infrastructure.redis.redis_pubsub import RedisPubSub


class CancelJobUseCase(UseCase):
    def __init__(
            self,
            repository: JobRepository,
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            repository=repository,
            redis_pubsub=redis_pubsub,
            logger=logger
        )

    def _execute(self, job: Job) -> Job:
        """
        Executes job cancellation. Marks job as CANCELLED and attempts to stop any
        ongoing download or processing.
        """

        if (job.status in FAILED_STATUSES) or (job.status in [JobStatus.FINISHED, JobStatus.CANCELLED]):
            self._logger.warning(f"Job {job.id} is not running anymore - status {job.status}, cannot cancel.")
            return job

        job.mark_cancelled(cancel_reason="User canceled")
        self._save_job(job)
        self._logger.info(f"Job {job.id} marked as CANCELLED")

        return job
