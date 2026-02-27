from ..core.celery_app import celery
from ..repositories.mongo_job_repository import MongoJobRepository

@celery.task(queue='process_task_queue')
def process_task(job_id: str):
    repo = MongoJobRepository()
    job = repo.get(job_id)
    job.process_data()
    repo.save(job)
    return job.id
