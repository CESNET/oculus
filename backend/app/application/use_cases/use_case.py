import logging
from typing import Optional

from .exceptions import CheckJobUseCaseFailedException
from ...domain import Job, JobRepository, JobStatus, FAILED_STATUSES
from ...infrastructure.redis.redis_pubsub import RedisPubSub
from ...settings import settings


class UseCase:
    def __init__(self, repository: JobRepository, redis_pubsub: RedisPubSub, logger: Optional[logging.Logger] = None):
        self._repository = repository
        self._redis_pubsub: RedisPubSub = redis_pubsub
        self._logger = logger or logging.getLogger(settings.APP_NAME)

    def _save_job(self, job: Job):
        self._repository.save(job)
        self._redis_pubsub.publish(job.id, job.status)

    def _execute(self, job: Job) -> Job:
        ...

    def execute(self, job_id: Optional[str]) -> str:
        if not job_id:
            raise ValueError("Job ID is required")

        job = self._repository.get(job_id)

        try:
            job = self._execute(job)
        except CheckJobUseCaseFailedException:
            raise
        except Exception as e:
            if job.status not in FAILED_STATUSES:
                job.status = JobStatus.FAILED
                job.fail_reason = f"Exception: {e}"

            self._save_job(job)

        return job.id
