import logging

from .application.orchestrators import BaseOrchestrator, CeleryOrchestrator
from .application.use_cases.cleanup_job_use_case import CleanupJobUseCase
from .application.use_cases.create_job_use_case import CreateJobUseCase
from .application.use_cases.download_job_use_case import DownloadJobUseCase
from .application.use_cases.finalize_job_use_case import FinalizeJobUseCase
from .application.use_cases.process_job_use_case import ProcessJobUseCase
from .config import APP_NAME
from .domain.job_repository import JobRepository
from .infrastructure.db.mongo_job_repository import MongoJobRepository
from .infrastructure.processors.gjtiff_processor import GJTIFFProcessor

default_job_repository = MongoJobRepository()
default_orchestrator = CeleryOrchestrator()
default_logger = logging.getLogger(APP_NAME)


class BootstrapContainer:
    def __init__(
            self,
            repository: JobRepository = None,
            orchestrator: BaseOrchestrator = None,
            logger: logging.Logger = None
    ):
        self._repository = repository or MongoJobRepository()
        self._orchestrator = orchestrator or CeleryOrchestrator()
        self._logger = logger or logging.getLogger(APP_NAME)

    @property
    def repository(self) -> JobRepository:
        return self._repository

    @property
    def orchestrator(self) -> BaseOrchestrator:
        return self._orchestrator

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def create_job(self) -> CreateJobUseCase:
        return CreateJobUseCase(
            repository=self._repository,
            orchestrator=self._orchestrator
        )

    def download_job(self) -> DownloadJobUseCase:
        return DownloadJobUseCase(
            repository=self._repository,
        )

    def process_job(self) -> ProcessJobUseCase:
        return ProcessJobUseCase(
            repository=self._repository,
            processor_class=GJTIFFProcessor
        )

    def finalize_job(self) -> FinalizeJobUseCase:
        return FinalizeJobUseCase(
            repository=self._repository,
        )

    def cleanup_job(self) -> CleanupJobUseCase:
        return CleanupJobUseCase(
            repository=self._repository,
        )


bootstrap_container = BootstrapContainer(
    repository=default_job_repository,
    orchestrator=default_orchestrator,
    logger=default_logger
)
