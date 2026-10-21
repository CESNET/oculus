import logging
from typing import Optional, Type

from .use_case import UseCase
from ...domain import (
    Job,
    JobRepository,
    FeatureStateRepository,
    FeatureStateLockRepository,
    FeatureStateLockType,
)
from ...infrastructure.processors import (
    Processor,
    visualization_helper_factory
)
from ...infrastructure.redis import RedisPubSub


class ProcessJobUseCase(UseCase):

    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: FeatureStateRepository,
            feature_state_lock_repository: FeatureStateLockRepository,
            processor_class: Type[Processor],
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger,
        )

        self._feature_state_repository = feature_state_repository
        self._feature_state_lock_repository = feature_state_lock_repository
        self._processor_class = processor_class

    def _execute(self, job: Job) -> Job:

        job.mark_waiting_for_processing_lock()
        job = self._save_job(job)

        try:
            with self._feature_state_lock_repository.lock(
                    feature_state_id=job.feature_state_id,
                    lock_type=FeatureStateLockType.PROCESSING,
            ):
                job.mark_processing()
                job = self._save_job(job)

                feature_state = self._feature_state_repository.get(job.feature_state_id)

                processor = self._processor_class(
                    job=job,
                    feature_state=feature_state,
                    visualization_helper=visualization_helper_factory.get_visualization_helper(
                        job=job,
                        feature_state=feature_state
                    ),
                    logger=self._logger,
                )

                processor.process()

                self._feature_state_repository.save(feature_state)

                job.mark_processing_complete()

        except Exception as e:
            job.mark_processing_failed(str(e))
            self._logger.exception(f"Processing failed for job {job.id}: {e}")

        return self._save_job(job)
