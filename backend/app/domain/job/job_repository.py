from abc import abstractmethod

from .job import Job
from ..common.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):
    """
    Repository abstraction for Job persistence.
    """

    def save(self, job: Job):
        """
        Save job entity.
        Version-based concurrency control is handled in concrete implementation.
        """
        self._save(job)

    @abstractmethod
    def _save(self, job: Job):
        """
        Persist job to storage backend.
        Must implement optimistic locking using job.version.
        """
        pass