import logging
from typing import Optional

from .use_case import UseCase
from ...domain import Job, JobRepository, FeatureState, FeatureStateRepository
from ...infrastructure.downloading import download_service_factory


class DownloadJobUseCase(UseCase):
    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: FeatureStateRepository,
            redis_pubsub,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger,
        )

        self._feature_state_repository = feature_state_repository

    def _execute(self, job: Job) -> Job:
        job.mark_downloading()
        self._save_job(job)

        feature_state: FeatureState = self._feature_state_repository.get_by_dataset(
            dataset=job.dataset.dataset_name,
            feature_id=job.feature_id
        )

        download_service = download_service_factory.get_download_service(job=job, feature_state=feature_state)

        try:
            # -------------------------
            # LOAD STATE
            # -------------------------
            feature_state = self._feature_state_repository.get_by_dataset(
                job.dataset.dataset_name,
                job.feature_id,
            )

            # -------------------------
            # DOWNLOAD
            # -------------------------
            downloaded_files = download_service.download(
                already_downloaded=feature_state.downloaded_files
            )

            # -------------------------
            # UPDATE STATE
            # -------------------------
            feature_state.add_downloaded_files(downloaded_files)
            self._feature_state_repository.save(feature_state)

            if not feature_state.downloaded_files:
                raise ValueError("No data downloaded / no data available locally")

            self._logger.info(f"Available files: {feature_state.downloaded_files}")

            # -------------------------
            # UPDATE JOB
            # -------------------------
            job.mark_downloading_complete(downloaded_files)

            self._logger.info(
                f"Downloading finished successfully for job {job.id}"
            )

        except Exception as e:
            job.mark_downloading_failed(str(e))
            self._logger.exception(
                f"Downloading failed for job {job.id}: {e}"
            )

        self._save_job(job)
        return job
