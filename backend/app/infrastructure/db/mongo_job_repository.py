from datetime import datetime, timezone

from ...domain.job import Job, JobRepository
from .mongo import mongo_provider


class MongoJobRepository(JobRepository):

    def __init__(self):
        self.collection = mongo_provider.get_collection("jobs")

    def get(self, job_id: str) -> Job:
        doc = self.collection.find_one({"_id": job_id})
        if not doc:
            raise ValueError("Job not found")

        self.collection.update_one(
            {"_id": job_id},
            {"$set": {"last_accessed": datetime.now(timezone.utc)}}
        )

        return Job.deserialize(doc)

    def _save(self, job: Job):
        data = job.serialize()
        data["last_accessed"] = datetime.now(timezone.utc)

        self.collection.update_one(
            {"_id": job.id},
            {"$set": data},
            upsert=True
        )

    def find_expired(self, threshold: datetime):
        return list(self.collection.find(
            {"last_accessed": {"$lt": threshold}}
        ))

    def delete(self, job_id: str):
        self.collection.delete_one({"_id": job_id})