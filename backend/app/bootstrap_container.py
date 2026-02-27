import logging

from .application.use_cases.cleanup_use_case import CleanupJobUseCase
from .application.use_cases.download_job_use_case import DownloadJobUseCase
from .application.use_cases.finalize_job_use_case import FinalizeJobUseCase
from .application.use_cases.process_job_use_case import ProcessJobUseCase
from .config import APP_NAME
from .domain.job_repository import JobRepository
from .infrastructure.db.mongo_job_repository import MongoJobRepository
from .infrastructure.downloaders.cdse_downloader import CDSEDownloader
from .infrastructure.processors.gjtiff_processor import GJTIFFProcessor


class BootstrapContainer:
    def __init__(
            self,
            repository: JobRepository = None,
            logger: logging.Logger = None
    ):
        self._repository = repository or MongoJobRepository()
        self._logger = logger or logging.getLogger(APP_NAME)

    def download_job(self) -> DownloadJobUseCase:
        return DownloadJobUseCase(
            repository=self._repository,
            downloader_class=CDSEDownloader,
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


bootstrap_container = BootstrapContainer()
