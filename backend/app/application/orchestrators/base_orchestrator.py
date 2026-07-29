import logging
from abc import ABC, abstractmethod

from ...domain import JobId

from ...settings import settings


class BaseOrchestrator(ABC):
    _logger: logging.Logger = logging.getLogger(settings.APP_NAME)

    @abstractmethod
    def run_pipeline(self, job_id: JobId):
        pass

    @abstractmethod
    def cleanup(self):
        pass
