from typing import Protocol

from .job import Job, JobId


class JobRepository(Protocol):

    def get(
            self,
            job_id: JobId
    ) -> Job:
        ...

    def save(
            self,
            job: Job
    ) -> Job:
        ...

    def delete (
            self,
            job_id: JobId
    ) -> None:
        ...