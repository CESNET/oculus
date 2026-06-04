from pymongo import ReturnDocument
from pymongo.collection import Collection

from ...domain import ConcurrencyError, JobNotFound, Job, JobId, JobDataset, JobRepository, JobStatus


class MongoJobRepository(JobRepository):

    def __init__(self, collection: Collection):
        self.collection = collection

    def _to_doc(self, job: Job) -> dict:
        return {
            "_id": str(job.id),
            "feature_id": job.feature_id,
            "dataset": job.dataset.name,
            "metadata": job.metadata,
            "request_properties": job.request_properties,
            "traversed_statuses": [status.name for status in job.traversed_statuses],
            "available_downloaded_files": job.available_downloaded_files,
            "available_processed_files": job.available_processed_files,
            "version": job.version,
            "created_at": job.created_at,
            "last_accessed": job.last_accessed,
            "fail_reasons": job.fail_reasons,
            "cancel_reason": job.cancel_reason,
        }

    def _from_doc(self, doc: dict) -> Job:
        traversed_statuses = [JobStatus(status_name) for status_name in doc.get("traversed_statuses", [])]

        return Job(
            id=JobId.from_str(doc["_id"]),
            feature_id=doc["feature_id"],
            dataset=JobDataset.from_str(doc["dataset"]),
            metadata=doc["metadata"],
            request_properties=doc["request_properties"],
            traversed_statuses=traversed_statuses,
            available_downloaded_files=doc["available_downloaded_files"],
            available_processed_files=doc["available_processed_files"],
            version=doc.get("version", 0),
            created_at=doc["created_at"],
            last_accessed=doc["last_accessed"],
            fail_reasons=doc.get("fail_reasons"),
            cancel_reason=doc.get("cancel_reason"),
        )

    def get(self, job_id: JobId) -> Job:
        doc = self.collection.find_one({"_id": str(job_id)})

        job = self._from_doc(doc)

        if job is None:
            raise JobNotFound(f"Job {job_id} was not found")

        return job

    def insert(self, job: Job) -> None:
        self.collection.insert_one(self._to_doc(job))

    def update(self, job: Job) -> Job:
        result = self.collection.find_one_and_update(
            filter={
                "_id": str(job.id),
                "version": job.version,
            },
            update={
                "$set": {
                    **self._to_doc(job),
                    "version": job.version + 1,
                }
            },
            return_document=ReturnDocument.AFTER,
        )

        if result is None:
            raise ConcurrencyError(f"Job {job.id} was modified concurrently")

        job = self._from_doc(result)

        return job
