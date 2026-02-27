from abc import ABC, abstractmethod


class BaseOrchestrator(ABC):

    @abstractmethod
    def run_pipeline(self, job_id: str):
        pass

    @abstractmethod
    def cleanup(self):
        pass
