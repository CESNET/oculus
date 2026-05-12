from datetime import datetime, timezone

from pymongo import ReturnDocument

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

        current_version = job.version

        data = job.serialize()
        data["last_accessed"] = datetime.now(timezone.utc)
        data.pop("version", None)

        # INSERT path (new job)
        if current_version == 0:
            self._get_collection().insert_one({
                **data,
                "version": 0
            })

            job.version = 0
            return

        # UPDATE path (existing job) - optimistic locking
        updated = self._get_collection().find_one_and_update(
            {
                "_id": job.id,
                "version": current_version
            },
            {
                "$set": data,
                "$inc": {"version": 1}
            },
            return_document=ReturnDocument.AFTER
        )

        if updated is None:
            current = self._get_collection().find_one(
                {"_id": job.id},
                {"version": 1}
            )

            db_version = current.get("version") if current else None

            raise ValueError(
                f"Optimistic lock failed for job {job.id} "
                f"(expected version {current_version}, db version {db_version})"
            )

        job.version = updated["version"]

    def find_expired(self, threshold: datetime):
        return list(self._get_collection().find(
            {"last_accessed": {"$lt": threshold}}
        ))

    def delete(self, job_id: str):
        self._get_collection().delete_one(
            {"_id": job_id}
        )
