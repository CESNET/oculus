from ..orchestrators import BaseOrchestrator
from ...domain import Job, JobDataset, JobRepository
from ...settings import settings


class CreateJobUseCase:
    def __init__(
            self,
            repository: JobRepository,
            orchestrator: BaseOrchestrator,
            data_directory_root: str
    ):
        self.repository = repository
        self.orchestrator = orchestrator

        self.data_directory_root = data_directory_root


    def execute(self, dataset: str, metadata: dict, properties: dict) -> str:
        if dataset not in settings.ENABLED_DATASETS:
            raise ValueError("Requested dataset is not enabled!")

        job = Job.create(
            dataset=JobDataset(dataset),
            metadata=metadata,
            properties=properties,
            data_directory=self.data_directory_root
        )

        self.repository.save(job)

        self.orchestrator.run_pipeline(job.id)

        return job.id
