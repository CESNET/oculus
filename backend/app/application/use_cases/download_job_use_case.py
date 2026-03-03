import logging
from typing import Optional

from .use_case import UseCase
from ...domain.job import Job
from ...domain.job_repository import JobRepository
from ...infrastructure.downloaders import Downloader
from ...infrastructure.downloaders import DownloaderSelector


class DownloadJobUseCase(UseCase):
    def __init__(
            self,
            repository: JobRepository,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(repository, logger)

    def execute(self, job_id: Optional[str]) -> str:
        if not job_id:
            raise ValueError("Job ID is required")

        job: Job = self._repository.get(job_id)

        job.mark_downloading()
        self._repository.save(job)

        downloader: Downloader = DownloaderSelector(job.dataset).select()(job=job)

        self._logger.info(f"Downloading job {job.id}")
        downloaded_data_path: str = downloader.download()

        job.mark_downloading_complete(downloaded_data_path)
        self._repository.save(job)

        self._logger.info(f"Job {job.id} downloaded to {downloaded_data_path}")

        return job.id
