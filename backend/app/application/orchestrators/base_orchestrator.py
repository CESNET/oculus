import logging
from abc import ABC, abstractmethod

from ...config import APP_NAME


class BaseOrchestrator(ABC):
    _logger: logging.Logger = logging.getLogger(APP_NAME)

    @abstractmethod
    def run_pipeline(self, job_id: str):
        pass

    @abstractmethod
    def cleanup(self):
        pass
