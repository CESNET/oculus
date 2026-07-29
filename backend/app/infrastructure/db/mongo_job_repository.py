from pymongo.collection import Collection

from ...domain import (
    Job,
    JobId,
    JobNotFound,
    JobRepository,
)


class MongoJobRepository(
    JobRepository
):

    def __init__(
            self,
            collection: Collection,
    ):
        self.collection = collection

    def _to_doc(
            self,
            job: Job,
    ) -> dict:
        doc = job.to_dict()
        doc["_id"] = str(job.id)

        return doc

    def _from_doc(
            self,
            doc: dict,
    ) -> Job:
        return Job.from_dict(
            JobId.parse(doc["_id"]),
            doc,
        )

    def get(
            self,
            job_id: JobId,
    ) -> Job:
        doc = self.collection.find_one(
            {"_id": str(job_id)}
        )

        if doc is None:
            raise JobNotFound(f"Job {job_id} was not found")

        return self._from_doc(doc)

    def save(
            self,
            job: Job,
    ) -> Job:
        # replace_one with upsert=True; if the document doesn't exist, it will be created, otherwise it will be updated

        result = self.collection.replace_one(
            {"_id": str(job.id)},
            self._to_doc(job),
            upsert=True,
        )

        if not result.acknowledged:
            raise RuntimeError("Failed to save job")

        return job

    def delete(
            self,
            job_id: JobId,
    ) -> None:
        result = self.collection.delete_one(
            {"_id": str(job_id)}
        )

        if result.deleted_count == 0:
            raise JobNotFound(f"Job {job_id} was not found")
