import logging
from typing import Type, Optional

from ...infrastructure import ProcessingBatch
from .use_case import UseCase
from ...domain import (
    Job,
    JobRepository,
    FeatureStateRepository,
    FeatureState,
    FeatureStateLockRepository,
    FeatureStateLockType,
    ProcessorOutput,
)
from ...infrastructure.processors import Processor
from ...infrastructure.redis import RedisPubSub


class ProcessJobUseCase(UseCase):

    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: FeatureStateRepository,
            feature_state_lock_repository: FeatureStateLockRepository,
            processor_class: Type[Processor],
            redis_pubsub: RedisPubSub,
            logger: Optional[logging.Logger] = None,
    ):
        super().__init__(
            job_repository=job_repository,
            redis_pubsub=redis_pubsub,
            logger=logger,
        )

        self._processor_class = processor_class

        self._feature_state_repository: FeatureStateRepository = feature_state_repository
        self._feature_state_lock_repository: FeatureStateLockRepository = feature_state_lock_repository

    def _execute(self, job: Job) -> Job:

        job.mark_waiting_for_processing_lock()
        job = self._save_job(job)

        try:
            with self._feature_state_lock_repository.lock(
                    feature_state_id=job.feature_state_id,
                    lock_type=FeatureStateLockType.PROCESSING
            ):
                job.mark_processing()
                job = self._save_job(job)

                feature_state = self._feature_state_repository.get(job.feature_state_id)

                processor: Processor = self._processor_class(
                    job=job,
                    feature_state=feature_state,
                    logger=self._logger,
                )

                files_to_process: ProcessingBatch = processor.get_files_to_process()

                if not files_to_process.files:
                    self._logger.info(f"No files to process for job {job.id}")

                    job.mark_processing_complete()

                else:
                    processor_outputs = self._process_files(processor=processor)

                    feature_state = self._update_feature_state(
                        feature_state=feature_state,
                        processor_outputs=processor_outputs,
                    )

                    job.mark_processing_complete()

        except Exception as e:
            job.mark_processing_failed(str(e))
            self._logger.exception(f"Processing failed for job {job.id}: {e}")

        job = self._save_job(job)
        return job

    def _process_files(
            self,
            processor: Processor,
    ) -> list[ProcessorOutput]:
        processor_outputs: list[ProcessorOutput] = processor.process()

        self._logger.info(f"Processed {len(processor_outputs)} files. Will update feature state.")

        return processor_outputs

    def _update_feature_state(
            self,
            feature_state: FeatureState,
            processor_outputs: list[ProcessorOutput],
    ) -> FeatureState:

        self._logger.info(f"Updating feature state of {feature_state.id}.")

        for output in processor_outputs:
            print(output)
            feature_state.set_file_processed_path(
                file=output.source_file,
                group=output.group,
                format_name=output.format_name,
                path=output.path,
                zoom_levels=output.zoom_levels,
            )

        self._feature_state_repository.save(feature_state)

        return feature_state
