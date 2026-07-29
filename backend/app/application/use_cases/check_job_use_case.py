import logging
from typing import Optional

from .exceptions import (
    CheckJobUseCaseFailedException,
    CheckJobUseCaseCancelledException,
)
from .use_case import UseCase
from ...domain import Job, JobRepository, JobStatus, FAILED_STATUSES
from ...infrastructure.redis.redis_pubsub import RedisPubSub


class CheckJobUseCase(UseCase):
    def __init__(
            self,
            job_repository: JobRepository,
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger,
        )

    def _execute(self, job: Job) -> Job:
        if job.current_status in FAILED_STATUSES:
            raise CheckJobUseCaseFailedException(
                job_id=job.id,
                status=job.current_status,
                fail_reason=job.last_fail_reason,
            )

        if job.current_status == JobStatus.CANCELLED:
            raise CheckJobUseCaseCancelledException(
                job_id=job.id,
                status=job.current_status,
                cancel_reason=job.cancel_reason,
            )

        return job
