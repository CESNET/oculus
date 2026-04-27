import logging
from typing import Optional

from domain import FeatureStateRepository
from .use_case import UseCase
from ...domain import Job, JobRepository
from ...infrastructure.downloaders import Downloader, downloader_factory
from ...infrastructure.redis.redis_pubsub import RedisPubSub


class DownloadJobUseCase(UseCase):
    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: FeatureStateRepository,
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            job_repository=job_repository,
            feature_state_repository=feature_state_repository,
            redis_pubsub=redis_pubsub,
            logger=logger
        )

    def _execute(self, job: Job) -> Job:
        job.mark_downloading()
        self._save_job(job)

        downloader: Downloader = downloader_factory.get_downloader(job)

        try:
            downloaded_files: list[str] = downloader.download()

            if not downloaded_files:
                raise ValueError("No data downloaded")

            job.mark_downloading_complete(downloaded_files)
            self._logger.info(f"Downloading finished successfully for job {job.id}")

        except Exception as e:
            job.mark_downloading_failed(str(e))
            self._logger.exception(f"Downloading failed for job {job.id}: {e}")

        self._save_job(job)

        return job
