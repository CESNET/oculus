import logging

import redis

from .application.orchestrators import BaseOrchestrator, CeleryOrchestrator
from .application.use_cases.cancel_job_use_case import CancelJobUseCase
from .application.use_cases.check_job_use_case import CheckJobUseCase
from .application.use_cases.cleanup_job_use_case import CleanupJobUseCase
from .application.use_cases.create_job_use_case import CreateJobUseCase
from .application.use_cases.download_job_use_case import DownloadJobUseCase
from .application.use_cases.finalize_job_use_case import FinalizeJobUseCase
from .application.use_cases.process_job_use_case import ProcessJobUseCase
from .domain.job.job_repository import JobRepository
from .domain.feature_state.feature_state_repository import FeatureStateRepository
from .infrastructure.db.mongo_job_repository import MongoJobRepository
from .infrastructure.db.mongo_feature_state_repository import MongoFeatureStateRepository
from .infrastructure.processors.gjtiff_processor import GJTIFFProcessor
from .infrastructure.redis.redis import get_redis_client
from .infrastructure.redis.redis_pubsub import RedisPubSub
from .settings import settings

default_job_repository = MongoJobRepository()
default_product_repository = MongoFeatureStateRepository()
default_orchestrator = CeleryOrchestrator()
default_redis_client = get_redis_client()
default_logger = logging.getLogger(settings.APP_NAME)


class BootstrapContainer:
    def __init__(
            self,
            job_repository: JobRepository = None,
            product_repository: FeatureStateRepository = None,
            orchestrator: BaseOrchestrator = None,
            redis_client: redis.Redis = None,
            logger: logging.Logger = None
    ):
        self._job_repository = job_repository or MongoJobRepository()
        self._product_repository = product_repository or MongoFeatureStateRepository()
        self._orchestrator = orchestrator or CeleryOrchestrator()
        self._redis_pubsub: RedisPubSub = RedisPubSub(client=redis_client) or RedisPubSub(default_redis_client)
        self._logger = logger or logging.getLogger(settings.APP_NAME)

    @property
    def job_repository(self) -> JobRepository:
        return self._job_repository

    @property
    def product_repository(self) -> FeatureStateRepository:
        return self._product_repository

    @property
    def orchestrator(self) -> BaseOrchestrator:
        return self._orchestrator

    @property
    def redis_pubsub(self) -> RedisPubSub:
        return self._redis_pubsub

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def create_job(self) -> CreateJobUseCase:
        return CreateJobUseCase(
            job_repository=self.job_repository,
            product_repository=self.product_repository,
            orchestrator=self.orchestrator,
            data_directory_root=settings.DATA_DIR
        )

    def check_job(self) -> CheckJobUseCase:
        return CheckJobUseCase(
            job_repository=self.job_repository,
            redis_pubsub=self.redis_pubsub
        )

    def download_job(self) -> DownloadJobUseCase:
        return DownloadJobUseCase(
            job_repository=self.job_repository,
            redis_pubsub=self.redis_pubsub
        )

    def process_job(self) -> ProcessJobUseCase:
        return ProcessJobUseCase(
            job_repository=self.job_repository,
            redis_pubsub=self.redis_pubsub,
            processor_class=GJTIFFProcessor
        )

    def finalize_job(self) -> FinalizeJobUseCase:
        return FinalizeJobUseCase(
            job_repository=self.job_repository,
            redis_pubsub=self.redis_pubsub
        )

    def cancel_job(self) -> CancelJobUseCase:
        return CancelJobUseCase(
            job_repository=self.job_repository,
            redis_pubsub=self.redis_pubsub
        )

    def cleanup_job(self) -> CleanupJobUseCase:
        return CleanupJobUseCase(
            job_repository=self.job_repository,
            redis_pubsub=self.redis_pubsub
        )


bootstrap_container = BootstrapContainer(
    job_repository=default_job_repository,
    orchestrator=default_orchestrator,
    redis_client=default_redis_client,
    logger=default_logger
)
