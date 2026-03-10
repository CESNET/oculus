import logging
from typing import Type, Optional

from .use_case import UseCase
from ...domain import Job, JobRepository
from ...infrastructure.processors import Processor


class ProcessJobUseCase(UseCase):
    def __init__(
            self,
            repository: JobRepository,
            processor_class: Type[Processor],
            logger: Optional[logging.Logger] = None
    ):
        self._processor_class: Type[Processor] = processor_class

        super().__init__(repository, logger)

    def execute(self, job_id: str) -> str:
        if not job_id:
            raise ValueError("Job ID is required")

        job: Job = self._repository.get(job_id)

        job.mark_processing()
        self._repository.save(job)

        processor = self._processor_class(job=job, logger=self._logger)

        try:
            processed_files: list[str] = processor.process()

            job.mark_processing_complete(processed_files)
            self._logger.info(f"Processing finished successfully for job {job_id}")

        except Exception as e:
            job.mark_processing_failed(str(e))
            self._logger.exception(f"Processing failed for job {job.id}: {e}")

        self._repository.save(job)

        return job.id
