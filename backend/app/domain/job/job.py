import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from .job_dataset import JobDataset
from .job_status import JobStatus, can_transition


class Job:
    def __init__(
            self,
            id: str,

            feature_id: str,
            dataset: JobDataset,

            metadata: dict,
            request_properties: dict,

            status: JobStatus,

            created_at: datetime,
            last_accessed: datetime,

            fail_reason: Optional[str] = None,
            cancel_reason: Optional[str] = None,
    ):
        self.id: str = id

        self.feature_id: str = feature_id
        self.dataset: JobDataset = dataset

        self.metadata: dict = metadata
        self.request_properties: dict = request_properties

        self.previous_status: Optional[JobStatus] = None
        self.status: JobStatus = status

        self.created_at: datetime = created_at
        self.last_accessed: datetime = last_accessed

        self.fail_reason: Optional[str] = fail_reason
        self.cancel_reason: Optional[str] = cancel_reason

    # ------------------------------------------------
    # helper methods
    # ------------------------------------------------

    def get_tile_path(self, processed_file: str, zoom: int, x: int, y: int) -> str:
        """
        Returns path to the tile in WebMercator mosaic file path
        Expected structure:
        <processed_file>/<zoom>/<x>/<y>.{processed_file_extension}
        """
        from pathlib import Path

        p = Path(processed_file)
        base_path = str(p.with_suffix(''))
        extension = p.suffix

        return os.path.join(base_path, str(zoom), str(x), f"{y}{extension}")

    # ------------------------------------------------
    # lifecycle helpers
    # ------------------------------------------------

    def touch(self):
        """
        Update last access timestamp.
        """
        self.last_accessed = datetime.now(timezone.utc)

    def transition(self, to_status: JobStatus):
        self.previous_status = self.status

        if self.status == JobStatus.CANCELLED:
            return

        if not can_transition(from_status=self.status, to_status=to_status):
            self.status = JobStatus.FAILED
            self.fail_reason = f"Invalid transition {self.status} -> {to_status}"

            raise ValueError(self.fail_reason)

        self.status = to_status

        self.touch()

    # ------------------------------------------------
    # status helpers
    # ------------------------------------------------

    def mark_downloading(self):
        self.transition(JobStatus.DOWNLOADING)

    def mark_downloading_complete(self, downloaded_files: list[str]):
        self.downloaded_files = downloaded_files
        self.transition(JobStatus.DOWNLOADING_COMPLETE)

    def mark_downloading_failed(self, fail_reason: str):
        self.fail_reason = fail_reason
        self.transition(JobStatus.DOWNLOADING_FAILED)

    def mark_processing(self):
        self.transition(JobStatus.PROCESSING)

    def mark_processing_complete(self, processed_files: list[str]):
        self.processed_files = processed_files
        self.transition(JobStatus.PROCESSING_COMPLETE)

    def mark_processing_failed(self, fail_reason: str):
        self.fail_reason = fail_reason
        self.transition(JobStatus.PROCESSING_FAILED)

    def mark_finalizing(self):
        self.transition(JobStatus.FINALIZING)

    def mark_finalizing_failed(self, fail_reason: str):
        self.fail_reason = fail_reason
        self.transition(JobStatus.FINALIZING_FAILED)

    def mark_finished(self):
        self.transition(JobStatus.FINISHED)

    def mark_cancelled(self, cancel_reason: str):
        self.cancel_reason = cancel_reason
        self.transition(JobStatus.CANCELLED)

    # ------------------------------------------------
    # setters
    # ------------------------------------------------

    def set_available_zoom_levels(self, zoom_levels: list[int]):
        # TODO tohle se bude držet v nějaké doméně produktu, tady je to teď v tuhle chvíli placeholder
        self.available_zoom_levels = zoom_levels

    # ------------------------------------------------
    # creation
    # ------------------------------------------------

    @classmethod
    def create(
            cls,
            dataset: JobDataset,
            metadata: dict,
            properties: dict,
    ) -> "Job":

        now = datetime.now(timezone.utc)

        job_id = str(uuid.uuid4())
        feature_id = metadata[dataset.feature_id_key_name]

        return cls(
            id=job_id,
            feature_id=feature_id,
            dataset=dataset,
            metadata=metadata,
            request_properties=properties,
            status=JobStatus.ACCEPTED,
            created_at=now,
            last_accessed=now
        )

    # --- Serialization ---
    def serialize(self, touch: bool = True) -> dict:
        """
        Convert Job to dictionary.
        If touch=True, last_accessed timestamp is updated
        """
        if touch:
            self.touch()

        serialized_dict = {
            "_id": self.id,

            "feature_id": self.feature_id,
            "dataset": self.dataset.name,

            "metadata": self.metadata,
            "request_properties": self.request_properties,

            "status": self.status.name,

            "created_at": self.created_at,
            "last_accessed": self.last_accessed,

            "fail_reason": self.fail_reason,
            "cancel_reason": self.cancel_reason,
        }

        return serialized_dict

    @classmethod
    def deserialize(cls, doc: dict) -> "Job":
        return cls(
            id=doc["_id"],

            feature_id=doc["feature_id"],
            dataset=JobDataset.from_str(doc["dataset"]),

            metadata=doc["metadata"],
            request_properties=doc["request_properties"],

            status=JobStatus(doc["status"]),

            created_at=doc["created_at"],
            last_accessed=doc["last_accessed"],

            fail_reason=doc.get("fail_reason"),
            cancel_reason=doc.get("cancel_reason"),
        )
