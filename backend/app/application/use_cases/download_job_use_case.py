import logging
from typing import Optional

from .use_case import UseCase
from ...domain import Job, JobRepository
from ...infrastructure.downloaders import Downloader, downloader_factory


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

        downloader: Downloader = downloader_factory.get_downloader(job)

        self._logger.info(f"Downloading job {job.id}")
        downloaded_files: list[str] = downloader.download()

        job.mark_downloading_complete(downloaded_files)
        self._repository.save(job)

        self._logger.info(f"Total {len(downloaded_files)} for job {job.id} downloaded")

        return job.id
