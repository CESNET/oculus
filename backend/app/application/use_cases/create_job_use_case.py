from infrastructure.db.mongo_feature_state_repository import MongoFeatureRepositoryNotFoundException
from ..orchestrators import BaseOrchestrator
from ...domain import Job, JobDataset, JobRepository, FeatureState, calculate_uuid, FeatureStateRepository
from ...settings import settings


class CreateJobUseCase:
    def __init__(
            self,
            job_repository: JobRepository,
            product_repository: FeatureStateRepository,
            orchestrator: BaseOrchestrator,
            data_directory_root: str
    ):
        self.job_repository = job_repository
        self.product_repository = product_repository
        self.orchestrator = orchestrator
        self.data_directory_root = data_directory_root

    def execute(self, dataset: str, metadata: dict, properties: dict) -> str:
        job_dataset = JobDataset.from_str(dataset)

        if job_dataset.family.value not in settings.ENABLED_DATASETS:
            raise ValueError("Requested dataset is not enabled!")

        feature_id = metadata[job_dataset.feature_id_key_name]

        # 1. create product
        try:
            product = self.product_repository.get(
                entity_id=str(calculate_uuid(
                    dataset=dataset,
                    feature_id=feature_id
                )
            ))
        except MongoFeatureRepositoryNotFoundException:
            product = FeatureState.create(
                dataset=dataset,
                feature_id=feature_id,
                data_directory=self.data_directory_root,
            )
            self.product_repository.save(product)

        # 2. create job
        job = Job.create(
            dataset=job_dataset,
            metadata=metadata,
            properties=properties,
        )
        self.job_repository.save(job)

        # 3. start pipeline
        self.orchestrator.run_pipeline(job.id)

        return job.id
