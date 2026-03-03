from ...config import ENABLED_DATASETS
from ...domain import Job
from ...domain import JobDataset


class CreateJobUseCase:
    def __init__(self, repository, orchestrator):
        self.repository = repository
        self.orchestrator = orchestrator

    def execute(self, dataset: str, metadata: dict, properties: dict) -> str:
        if dataset not in ENABLED_DATASETS:
            raise ValueError("Requested dataset is not enabled!")

        job = Job.create(
            dataset=JobDataset(dataset),
            metadata=metadata,
            properties=properties
        )

        self.repository.save(job)

        self.orchestrator.run_pipeline(job.id)

        return job.id
