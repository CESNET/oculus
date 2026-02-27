from datetime import datetime, timezone

from ..domain import Job, JobStatus
from ..domain import JobRepository
from ..infrastructure.db.mongo import get_collection


class MongoJobRepository(JobRepository):

    def create(self, job_id: str) -> Job:
        now = datetime.now(tz=timezone.utc)
        job = Job(id=job_id, status=JobStatus.ACCEPTED, created_at=now)
        data = job.serialize()
        data["last_accessed"] = now
        get_collection().insert_one(data)
        return job

    def get(self, job_id: str) -> Job:
        doc = get_collection().find_one({"_id": job_id})
        if not doc:
            return None

        get_collection().find_one_and_update(
            {"_id": job_id},
            {"$set": {"last_accessed": datetime.now(tz=timezone.utc)}}
        )

        return Job.deserialize(doc)

    def save(self, job: Job):
        data = job.serialize()
        data["last_accessed"] = datetime.now(tz=timezone.utc)
        get_collection().find_one_and_update(
            {"_id": job.id},
            {"$set": data}
        )

    def find_expired(self, threshold: datetime):
        return list(get_collection().find({"last_accessed": {"$lt": threshold}}))

    def delete(self, job_id: str):
        get_collection().delete_one({"_id": job_id})
