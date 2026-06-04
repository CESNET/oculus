from typing import Protocol, Optional

from .job import Job, JobId


class JobRepository(Protocol):

    def get(self, job_id: JobId) -> Job:
        ...

    def insert(self, job: Job) -> None:
        ...

    def update(self, job: Job) -> Job:
        ...
