import logging
from typing import Optional

from .use_case import UseCase
from ...domain import Job, JobRepository, FeatureStateRepository, FeatureStateId
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
        job = self._save_job(job)

        feature_state_id = FeatureStateId.from_parts(
            dataset=job.dataset.name,
            feature_id=job.feature_id,
        )

        reserved_files: list[str] = []
        downloaded_files: list[str] = []

        try:
            # -------------------------
            # LOAD GLOBAL STATE
            # -------------------------
            feature_state = self._feature_state_repository.get(feature_state_id)

            download_service = download_service_factory.get_download_service(
                job=job,
                feature_state=feature_state,
            )

            # -------------------------
            # JOB INTENT (co chce job)
            # -------------------------
            job_wants = set(job.required_files)

            # -------------------------
            # GLOBAL REALITY (co existuje)
            # -------------------------
            available = set(download_service.discover_files())

            # -------------------------
            # INTERSECTION (co má smysl řešit)
            # -------------------------
            candidates = job_wants & available

            self._logger.info(
                f"Job wants {len(job_wants)} files, "
                f"available {len(available)}, "
                f"processing {len(candidates)}"
            )

            # -------------------------
            # RESERVE GLOBALLY (anti-concurrency)
            # -------------------------
            for file in candidates:
                ok = self._feature_state_repository.reserve_download(
                    feature_state_id=feature_state_id,
                    file=file,
                    job_id=str(job.id),
                )
                if ok:
                    reserved_files.append(file)

            # -------------------------
            # DOWNLOAD ONLY RESERVED
            # -------------------------
            downloaded_files = download_service.download(
                files=reserved_files
            )

            # -------------------------
            # COMMIT GLOBAL STATE
            # -------------------------
            for file in downloaded_files:
                ok = self._feature_state_repository.complete_download(
                    feature_state_id=feature_state_id,
                    file=file,
                    job_id=str(job.id),
                )
                if not ok:
                    raise RuntimeError(f"Failed commit for {file}")

            # -------------------------
            # RELEASE FAILED
            # -------------------------
            failed = set(reserved_files) - set(downloaded_files)

            for file in failed:
                self._feature_state_repository.release_download(
                    feature_state_id=feature_state_id,
                    file=file,
                    job_id=str(job.id),
                )

            # -------------------------
            # JOB VIEW (TOHLE je klíč)
            # -------------------------
            job.available_downloaded_files = list(
                job_wants & set(feature_state.downloaded_files)
            )

            job.mark_downloading_complete()

        except Exception as e:

            for file in reserved_files:
                if file not in downloaded_files:
                    self._feature_state_repository.release_download(
                        feature_state_id=feature_state_id,
                        file=file,
                        job_id=str(job.id),
                    )

            job.mark_downloading_failed(str(e))
            self._logger.exception(f"Download failed for job {job.id}: {e}")

        job = self._save_job(job)
        return job
