import logging
from typing import Type, Optional

from .use_case import UseCase

from ...domain import    Job,    JobRepository,   FeatureState,    FeatureStateId,    FeatureStateRepository

from ...infrastructure.processors import    Processor
from ...infrastructure.redis.redis_pubsub import    RedisPubSub


class ProcessJobUseCase(UseCase):

    def __init__(
        self,
        job_repository: JobRepository,
        feature_state_repository: FeatureStateRepository,
        processor_class: Type[Processor],
        redis_pubsub: RedisPubSub,
        logger: Optional[logging.Logger] = None,
    ):

        self._processor_class = processor_class

        self._feature_state_repository = (
            feature_state_repository
        )

        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger,
        )

    def _execute(
        self,
        job: Job,
    ) -> Job:

        # -------------------------
        # UPDATE JOB STATUS
        # -------------------------

        job.mark_processing()

        job = self._save_job(job)

        feature_state_id = (
            FeatureStateId.from_parts(
                dataset=job.dataset.name,
                feature_id=job.feature_id,
            )
        )

        reserved_files: list[str] = []

        try:

            # -------------------------
            # LOAD FEATURE STATE
            # -------------------------

            feature_state: FeatureState = (
                self._feature_state_repository.get(
                    feature_state_id
                )
            )

            # -------------------------
            # CREATE PROCESSOR
            # -------------------------

            processor = self._processor_class(
                job=job,
                feature_state=feature_state,
                logger=self._logger,
            )

            # -------------------------
            # DETERMINE CANDIDATES
            # -------------------------

            candidate_files = processor.get_candidate_files(
                already_processed=feature_state.processed_files
            )

            # -------------------------
            # RESERVE FILES
            # -------------------------

            reserved_files = (
                self._feature_state_repository
                .reserve_processing(
                    feature_state_id=feature_state_id,
                    files=candidate_files,
                )
            )

            if not reserved_files:

                self._logger.info(
                    "No files reserved for processing"
                )

                job.mark_processing_complete()

                return self._save_job(job)

            self._logger.info(
                f"Reserved processing files: "
                f"{reserved_files}"
            )

            # -------------------------
            # LONG RUNNING PROCESSING
            # -------------------------

            processed_files = processor.process(
                files=reserved_files
            )

            self._logger.info(
                f"Successfully processed files: "
                f"{processed_files}"
            )

            # -------------------------
            # COMPLETE SUCCESSFUL FILES
            # -------------------------

            if processed_files:

                self._feature_state_repository.complete_processing(
                    feature_state_id=feature_state_id,
                    files=processed_files,
                )

            # -------------------------
            # RELEASE FAILED FILES
            # -------------------------

            failed_files = list(
                set(reserved_files) - set(processed_files)
            )

            if failed_files:

                self._feature_state_repository.release_processing(
                    feature_state_id=feature_state_id,
                    files=failed_files,
                )

                self._logger.warning(
                    f"Released failed processing files: "
                    f"{failed_files}"
                )

            # -------------------------
            # VALIDATION
            # -------------------------

            updated_state = (
                self._feature_state_repository.get(
                    feature_state_id
                )
            )

            if not updated_state.processed_files:

                raise ValueError(
                    "No processed files available"
                )

            self._logger.info(
                f"Processed files: "
                f"{updated_state.processed_files}"
            )

            # -------------------------
            # SUCCESS
            # -------------------------

            job.mark_processing_complete()

            self._logger.info(
                f"Processing finished successfully "
                f"for job {job.id}"
            )

        except Exception as e:

            # -------------------------
            # RELEASE ALL RESERVED FILES
            # -------------------------

            if reserved_files:

                self._feature_state_repository.release_processing(
                    feature_state_id=feature_state_id,
                    files=reserved_files,
                )

            # -------------------------
            # UPDATE FAILURE
            # -------------------------

            job.mark_processing_failed(str(e))

            self._logger.exception(
                f"Processing failed for job {job.id}: {e}"
            )

        # -------------------------
        # SAVE FINAL JOB
        # -------------------------

        job = self._save_job(job)

        return job