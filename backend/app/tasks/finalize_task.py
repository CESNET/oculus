from ..core.celery_app import celery
from ..repositories.mongo_job_repository import MongoJobRepository


@celery.task
def finalize_task(job_id: str):
    repo = MongoJobRepository()
    job = repo.get(job_id)
    job.finalize()
    repo.save(job)
    return job.id
