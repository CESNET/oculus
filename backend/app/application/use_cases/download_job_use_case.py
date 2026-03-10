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
        self._save_job(job)

        downloader: Downloader = downloader_factory.get_downloader(job)

        try:
            downloaded_files: list[str] = downloader.download()

            if not downloaded_files:
                raise ValueError("No data downloaded")

            job.mark_downloading_complete(downloaded_files)
            self._logger.info(f"Downloading finished successfully for job {job_id}")

        except Exception as e:
            job.mark_downloading_failed(str(e))
            self._logger.exception(f"Downloading failed for job {job.id}: {e}")

        self._save_job(job)

        return job.id
