import logging
from typing import Optional

from ...domain import Job, JobRepository
from ...infrastructure.redis.redis_pubsub import redis_pubsub
from ...settings import settings


class UseCase:
    def __init__(self, repository: JobRepository, logger: Optional[logging.Logger] = None):
        self._repository = repository
        self._logger = logger or logging.getLogger(settings.APP_NAME)

    def _save_job(self, job: Job):
        self._repository.save(job)
        redis_pubsub.publish(job.id, job.status)

    def execute(self, job_id: Optional[str]) -> str:
        ...
        # raise NotImplementedError(f"Subclasses of {self.__class__.__name__} must implement execute(job_id)")
