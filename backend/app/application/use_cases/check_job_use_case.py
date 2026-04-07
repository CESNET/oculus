import logging
from typing import Optional

from .exceptions import *
from .use_case import UseCase
from ...domain import Job, JobRepository, FAILED_STATUSES, JobStatus
from ...infrastructure.redis.redis_pubsub import RedisPubSub


class CheckJobUseCase(UseCase):
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
        if job.status in FAILED_STATUSES:
            raise CheckJobUseCaseFailedException(job_id=job.id, status=job.status, fail_reason=job.fail_reason)

        if job.status == JobStatus.CANCELLED:
            raise CheckJobUseCaseCancelledException(job_id=job.id, status=job.status, cancel_reason=job.cancel_reason)

        return job
