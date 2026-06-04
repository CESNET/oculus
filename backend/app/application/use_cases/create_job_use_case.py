from ..orchestrators import BaseOrchestrator
from ...domain import FeatureState, Job, JobDataset, JobRepository, FeatureStateRepository
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

    def execute(self, dataset: str, metadata: dict, request_properties: dict) -> str:
        job_dataset = JobDataset.from_str(dataset)

        if job_dataset.family.value not in settings.ENABLED_DATASETS:
            raise ValueError("Dataset not enabled")

        feature_id = metadata[job_dataset.feature_id_key_name]

        # 1. FeatureState (atomic)
        feature_state = self.feature_state_repository.get_or_create(
            dataset=job_dataset.dataset_name,
            feature_id=feature_id,
            root_directory=self.data_directory_root,
        )

        # 2. Job
        job = Job.create(
            dataset=job_dataset,
            metadata=metadata,
            request_properties=request_properties,
        )

        self.job_repository.insert(job)

        # 3. pipeline
        self.orchestrator.run_pipeline(str(job.id))

        return str(job.id)
