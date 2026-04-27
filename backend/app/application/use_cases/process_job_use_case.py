import logging
from typing import Type, Optional

from .use_case import UseCase
from ...domain import Job, JobRepository
from ...infrastructure.processors import Processor
from ...infrastructure.redis.redis_pubsub import RedisPubSub


class ProcessJobUseCase(UseCase):
    def __init__(
            self,
            job_repository: JobRepository,
            processor_class: Type[Processor],
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None
    ):
        self._processor_class: Type[Processor] = processor_class

        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger
        )

    def _execute(self, job: Job) -> Job:
        job.mark_processing()
        self._save_job(job)

        processor = self._processor_class(job=job, logger=self._logger)

        try:
            processed_files: list[str] = processor.process()

            job.mark_processing_complete(processed_files)
            self._logger.info(f"Processing finished successfully for job {job.id}")

        except Exception as e:
            job.mark_processing_failed(str(e))
            self._logger.exception(f"Processing failed for job {job.id}: {e}")

        self._save_job(job)

        return job
