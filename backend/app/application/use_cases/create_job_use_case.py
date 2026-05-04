from ..orchestrators import BaseOrchestrator
from ...domain import FeatureState, Job, JobDataset, JobRepository, FeatureStateRepository
from ...infrastructure.db import MongoFeatureRepositoryNotFoundException
from ...settings import settings


class CreateJobUseCase:
    def __init__(
            self,
            job_repository: JobRepository,
            feature_state_repository: FeatureStateRepository,
            orchestrator: BaseOrchestrator,
            data_directory_root: str,
    ):
        self.job_repository = job_repository
        self.feature_state_repository = feature_state_repository
        self.orchestrator = orchestrator
        self.data_directory_root = data_directory_root

    def execute(self, dataset: str, metadata: dict, properties: dict) -> str:
        job_dataset = JobDataset.from_str(dataset)

        if job_dataset.family.value not in settings.ENABLED_DATASETS:
            raise ValueError("Requested dataset is not enabled!")

        feature_id = metadata[job_dataset.feature_id_key_name]

        # 1. create or get FeatureState
        try:
            feature_state = self.feature_state_repository.get_by_dataset(
                job_dataset.dataset_name,
                feature_id,
            )

        except MongoFeatureRepositoryNotFoundException:
            feature_state = self.feature_state_repository.save(
                FeatureState.create(
                    dataset=job_dataset.dataset_name,
                    feature_id=feature_id,
                    feature_root_directory=self.data_directory_root,
                )
            )

        # 2. create Job
        job = Job.create(
            dataset=job_dataset,
            metadata=metadata,
            properties=properties,
        )

        self.job_repository.save(job)

        # 3. start pipeline
        self.orchestrator.run_pipeline(job.id)

        return job.id
