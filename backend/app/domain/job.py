from datetime import datetime, timezone
from typing import Optional

from .job_status import JobStatus


class Job:
    def __init__(
            self,
            id: str,
            status: JobStatus,
            created_at: datetime,
            downloaded_data_path: Optional[str] = None,
            processed_data_path: Optional[str] = None,
            fail_reason: Optional[str] = None
    ):
        self.id: str = id
        self.status: JobStatus = status
        self.created_at: datetime = created_at
        self.downloaded_data_path: Optional[str] = downloaded_data_path
        self.processed_data_path: Optional[str] = processed_data_path
        self.fail_reason: Optional[str] = fail_reason

        self.allowed_transitions: dict[JobStatus, list[JobStatus]] = {
            JobStatus.ACCEPTED: [JobStatus.DOWNLOADING],
            JobStatus.DOWNLOADING: [JobStatus.DOWNLOADING_COMPLETE, JobStatus.DOWNLOADING_FAILED],
            JobStatus.DOWNLOADING_COMPLETE: [JobStatus.PROCESSING],
            JobStatus.DOWNLOADING_FAILED: [JobStatus.DOWNLOADING, JobStatus.FAILED],
            JobStatus.PROCESSING: [JobStatus.PROCESSING_COMPLETE, JobStatus.PROCESSING_FAILED],
            JobStatus.PROCESSING_COMPLETE: [JobStatus.FINALIZING],
            JobStatus.PROCESSING_FAILED: [JobStatus.PROCESSING, JobStatus.FAILED],
            JobStatus.FINALIZING: [JobStatus.FINISHED],
            JobStatus.FINALIZING_FAILED: [JobStatus.FINALIZING, JobStatus.FAILED],
            JobStatus.FINISHED: [],
            JobStatus.FAILED: [],
        }

    def transition(self, to_status: JobStatus):
        if to_status not in self.allowed_transitions[self.status]:
            raise ValueError(f"Invalid transition from {self.status} to {to_status}")
        self.status = to_status

    def mark_downloading(self):
        self.transition(JobStatus.DOWNLOADING)

    def mark_downloading_complete(self, downloaded_data_path: str):
        self.downloaded_data_path = downloaded_data_path
        self.transition(JobStatus.DOWNLOADING_COMPLETE)

    def mark_downloading_failed(self, fail_reason: str):
        self.fail_reason = fail_reason
        self.transition(JobStatus.DOWNLOADING_FAILED)

    def mark_processing(self):
        self.transition(JobStatus.PROCESSING)

    def mark_processing_complete(self, processed_data_path: str):
        self.processed_data_path = processed_data_path
        self.transition(JobStatus.PROCESSING_COMPLETE)

    def mark_processing_failed(self, fail_reason: str):
        self.fail_reason = fail_reason
        self.transition(JobStatus.PROCESSING_FAILED)

    def mark_finalizing(self):
        self.transition(JobStatus.FINALIZING)

    def mark_finalizing_failed(self):
        self.transition(JobStatus.FINALIZING_FAILED)

    def mark_finished(self):
        self.transition(JobStatus.FINISHED)

    # --- Serialization ---
    def serialize(self) -> dict:
        return {
            "_id": self.id,
            "status": self.status.value,
            "created_at": self.created_at,
            "downloaded_data_path": self.downloaded_data_path,
            "processed_data_path": self.processed_data_path,
            "fail_reason": self.fail_reason,
            "updated_at": datetime.now(tz=timezone.utc).isoformat(),
        }

    @classmethod
    def deserialize(cls, doc: dict) -> "Job":
        return cls(
            id=doc["_id"],
            status=JobStatus(doc["status"]),
            created_at=doc["created_at"],
            downloaded_data_path=doc.get("downloaded_data_path"),
            processed_data_path=doc.get("processed_data_path"),
            fail_reason=doc["fail_reason"]
        )
