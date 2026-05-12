from datetime import datetime, timezone

from .mongo import get_collection
from ...domain import Job, JobRepository


class MongoJobRepository(JobRepository):

    def _get_collection(self):
        return get_collection(collection_name="jobs")

    def get(self, job_id: str) -> Job:
        doc = self._get_collection().find_one({"_id": job_id})
        if not doc:
            raise ValueError("Job not found in the database")

        self._get_collection().find_one_and_update(
            {"_id": job_id},
            {"$set": {"last_accessed": datetime.now(tz=timezone.utc)}}
        )

        return Job.deserialize(doc)

    def _save(self, job: Job):
        now = datetime.now(tz=timezone.utc)

        data = job.serialize()
        data["last_accessed"] = now

        self._get_collection().update_one(
            {"_id": job.id},
            {"$set": data},
            upsert=True
        )

    def find_expired(self, threshold: datetime) -> list[Job]:
        return list(self._get_collection().find({"last_accessed": {"$lt": threshold}}))

    def delete(self, job_id: str):
        self._get_collection().delete_one({"_id": job_id})
