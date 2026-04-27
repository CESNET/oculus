import logging
from typing import Optional

from .exceptions import CheckJobUseCaseFailedException, CheckJobUseCaseCancelledException
from ...domain import Job, JobRepository, JobStatus, FAILED_STATUSES, FeatureStateRepository
from ...infrastructure.redis.redis_pubsub import RedisPubSub
from ...settings import settings


class UseCase:
    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: Optional[FeatureStateRepository],
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None
    ):
        self._job_repository: JobRepository = job_repository
        self._feature_state_repository: Optional[FeatureStateRepository] = feature_state_repository
        self._redis_pubsub: RedisPubSub = redis_pubsub
        self._logger = logger or logging.getLogger(settings.APP_NAME)

    def _save_job(self, job: Job):
        if job.previous_status:
            already_saved_job = self._job_repository.get(job.id)

            if already_saved_job.status != job.previous_status:
                raise ValueError(
                    f"Cannot save job {job.id}: expected status {job.previous_status} but got {already_saved_job.status} from DB!"
                )

            if already_saved_job.status == JobStatus.CANCELLED:
                pass

        self._job_repository.save(job)
        self._redis_pubsub.publish(job.id, job.status)

    def _execute(self, job: Job) -> Job:
        ...

    def execute(self, job_id: Optional[str]) -> str:
        if not job_id:
            raise ValueError("Job ID is required")

        job = self._job_repository.get(job_id)

        try:
            job = self._execute(job)

        except CheckJobUseCaseFailedException:
            raise

        except CheckJobUseCaseCancelledException:
            raise

        except Exception as e:
            if job.status not in FAILED_STATUSES:
                job.status = JobStatus.FAILED
                job.fail_reason = f"Exception: {e}"

            self._save_job(job)

        return job.id
