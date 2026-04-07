from abc import ABC, abstractmethod
from datetime import datetime

from .job_status import JobStatus
from .job import Job


class JobRepository(ABC):
    @abstractmethod
    def get(self, job_id: str) -> Job:
        pass

    def save(self, job: Job):
        """
        Save job with optional state check.
        Uloží jen pokud aktuální stav v DB odpovídá aktuálnímu stavu Jobu -> nic se nezměnilo pod rukama
        """
        if job.previous_status:
            already_saved_job = self.get(job.id)

            if already_saved_job.status == JobStatus.CANCELLED:
                return

            if already_saved_job.status != job.previous_status:
                raise ValueError(
                    f"Cannot save job {job.id}: expected status {job.previous_status} but got {already_saved_job.status} from DB!"
                )

        self._save(job)

    @abstractmethod
    def _save(self, job: Job):
        pass

    @abstractmethod
    def find_expired(self, threshold: datetime) -> list[Job]:
        pass

    @abstractmethod
    def delete(self, job_id: str):
        pass
