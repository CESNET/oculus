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

        # Update last access timestamp (non-critical metadata update)
        self.collection.update_one(
            {"_id": job_id},
            {"$set": {"last_accessed": datetime.now(timezone.utc)}}
        )

        return Job.deserialize(doc)

    def _save(self, job: Job):

        # TODO začni tady a nějak vyřeš to ukládání!!!

        current_version = job.version

        data = job.serialize()
        data["last_accessed"] = datetime.now(timezone.utc)
        data.pop("version", None)

        if current_version == 0:
            # INSERT path (new job)
            result = self.collection.insert_one({
                **data,
                "version": 0
            })

            job.version = 0
            return

        # UPDATE path (existing job)
        result = self.collection.update_one(
            {
                "_id": job.id,
                "version": current_version
            },
            {
                "$set": data,
                "$inc": {"version": 1}
            }
        )

        if result.matched_count == 0:
            raise ValueError(
                f"Optimistic lock failed for job {job.id} "
                f"(expected version {current_version})"
            )

        job.version += 1

    def find_expired(self, threshold: datetime):
        return list(self.collection.find(
            {"last_accessed": {"$lt": threshold}}
        ))

    def delete(self, job_id: str):
        self.collection.delete_one({"_id": job_id})