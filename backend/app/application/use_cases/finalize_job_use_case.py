import logging
from typing import Optional

from .use_case import UseCase
from ...domain import Job, JobRepository
from ...infrastructure.redis.redis_pubsub import RedisPubSub


class FinalizeJobUseCase(UseCase):
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
        job.mark_finalizing()
        self._save_job(job)

        self._logger.info(f"Finalizing job {job.id}")
        # TODO: tady bude něco jako vracení requestu zpět frontendu

        self._logger.info(f"Job {job.id} finished")

        job.mark_finished()
        self._save_job(job)

        return job
