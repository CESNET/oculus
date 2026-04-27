from abc import abstractmethod

from .job import Job
from ..common.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):

    def save(self, job: Job):
        current = self.get(job.id)
        if job.previous_status and current.status != job.previous_status:
            raise ValueError("Concurrency conflict")

        self._save(job)

    @abstractmethod
    def _save(self, job: Job):
        pass
