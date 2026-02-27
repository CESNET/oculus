# app/application/use_cases/process_job_use_case.py
import logging
from typing import Type, Optional

from .use_case import UseCase
from ...domain.job import Job
from ...domain.job_repository import JobRepository
from ...infrastructure.processors.processor import Processor


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

        processor: Processor = self._processor_class(job_id=job.id, logger=self._logger)
        self._logger.info(f"Processing job {job.id}")
        processor_output = processor.process()
        processed_data_path=processor_output # Todo něco v tom smyslu
        # TODO: zpracovat processor_output, uložit výsledky apod.

        job.mark_processing_complete(processed_data_path)
        self._repository.save(job)

        self._logger.info(f"Job {job.id} processed")
        return job.id
