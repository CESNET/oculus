import os
from datetime import datetime, timedelta, timezone

from ..core.celery_app import celery
from ..repositories.mongo_job_repository import MongoJobRepository


@celery.task
def cleanup_task():
    repo = MongoJobRepository()
    threshold = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
    expired_jobs = repo.find_expired(threshold)
    for job in expired_jobs:
        job_id = job["_id"]
        folder = f"/tmp/{job_id}"
        if os.path.exists(folder):
            pass
        repo.delete(job_id)
