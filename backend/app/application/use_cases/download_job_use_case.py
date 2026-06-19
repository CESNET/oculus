import logging
from typing import Optional

from .use_case import UseCase
from ...domain import (
    Job,
    JobRepository,
    FeatureStateRepository,
    FeatureState,
    FeatureStateLockRepository,
    FeatureStateLockType
)
from ...infrastructure.downloading import DownloadService, download_service_factory
from ...infrastructure.redis import RedisPubSub


class DownloadJobUseCase(UseCase):

    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: FeatureStateRepository,
            feature_state_lock_repository: FeatureStateLockRepository,
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger,
        )
        self._feature_state_repository: FeatureStateRepository = feature_state_repository
        self._feature_state_lock_repository: FeatureStateLockRepository = feature_state_lock_repository

    def _execute(self, job: Job) -> Job:
        """
        Stáhne všechny soubory definované ve feature_state.files, které ještě nejsou stažené.
        Klíče v files jsou názvy souborů s příponou (např. "B01.tif").
        """
        job.mark_waiting_for_download_lock()
        job = self._save_job(job)

        try:
            with self._feature_state_lock_repository.lock(
                    feature_state_id=job.feature_state_id,
                    lock_type=FeatureStateLockType.DOWNLOADING
            ):
                job.mark_downloading()
                job = self._save_job(job)

                feature_state: FeatureState = self._feature_state_repository.get(job.feature_state_id)
                download_service: DownloadService = download_service_factory.get_download_service(
                    job=job,
                    feature_state=feature_state,
                )

                requested_files = download_service.get_requested_files()
                job.set_requested_files(requested_files)

                files_to_download = download_service.get_files_to_download(requested_files=requested_files)

                if not files_to_download:
                    self._logger.info(f"No files to download for job {job.id}")
                    job.mark_downloading_complete()

                else:
                    downloaded_files = self._download_files(
                        download_service=download_service,
                        files_to_download=files_to_download,
                    )

                    feature_state = self._update_feature_state(
                        feature_state=feature_state,
                        downloaded_files=downloaded_files,
                    )

                    job.mark_downloading_complete()

        except Exception as e:
            job.mark_downloading_failed(str(e))
            self._logger.exception(f"Download failed for job {job.id}: {e}")

        job = self._save_job(job)
        return job

    def _download_files(
            self,
            download_service: DownloadService,
            files_to_download: list[str],
    ) -> list[str]:
        self._logger.info(f"Downloading {len(files_to_download)} files.")

        downloaded_files_paths = download_service.download(files_to_download)

        self._logger.info(f"Downloaded {len(downloaded_files_paths)} files. Will update feature state.")

        return downloaded_files_paths

    def _update_feature_state(
            self,
            feature_state: FeatureState,
            downloaded_files: list[str],
    ) -> FeatureState:
        self._logger.info(f"Updating feature state of {feature_state.id}.")

        feature_state = self._feature_state_repository.mark_files_downloaded(
            feature_state_id=feature_state.id,
            downloaded_files=downloaded_files,
        )
        return feature_state
