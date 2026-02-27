from abc import ABC, abstractmethod
from datetime import datetime

from . import Job


class JobRepository(ABC):

    @abstractmethod
    def create(self, job_id: str) -> Job:
        pass

    @abstractmethod
    def get(self, job_id: str) -> Job:
        pass

    @abstractmethod
    def save(self, job: Job):
        pass

    @abstractmethod
    def find_expired(self, threshold: datetime) -> list[Job]:
        pass

    @abstractmethod
    def delete(self, job_id: str):
        pass
