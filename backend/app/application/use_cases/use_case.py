import logging
from typing import Optional

from ...domain import Job, JobRepository, JobStatus, FAILED_STATUSES
from ...infrastructure.redis.redis_pubsub import RedisPubSub
from ...settings import settings


class UseCase:
    """
    Base class for job execution use cases.
    """

    def __init__(
            self,
            job_repository: JobRepository,
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None,
    ):
        self._job_repository = job_repository
        self._redis_pubsub = redis_pubsub
        self._logger = logger or logging.getLogger(settings.APP_NAME)

    def _save_job(self, job: Job):
        """
        Persist job and publish status update.
        """
        self._job_repository.save(job)
        self._redis_pubsub.publish(job.id, job.status)

    def _execute(self, job: Job) -> Job:
        """
        To be implemented by subclasses.
        """
        raise NotImplementedError

    def execute(self, job_id: str) -> str:
        """
        Entry point for job execution.
        """
        if not job_id:
            raise ValueError("Job ID is required")

        job = self._job_repository.get(job_id)

        try:
            job = self._execute(job)

        except Exception as e:
            if job.status not in FAILED_STATUSES:
                job.status = JobStatus.FAILED
                job.fail_reason = f"Exception: {e}"

            self._save_job(job)
            return job.id

        self._save_job(job)
        return job.id