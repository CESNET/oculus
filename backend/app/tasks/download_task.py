from ..core.celery_app import celery
from ..repositories.mongo_job_repository import MongoJobRepository


@celery.task
def download_task(job_id: str):
    import logging
    logging.getLogger("oculus").info(f"Download task job_id: {job_id}")
    repo = MongoJobRepository()
    job = repo.get(job_id)
    job.download_data()
    repo.save(job)
    return job.id
