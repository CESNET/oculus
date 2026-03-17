import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from .job_dataset import JobDataset
from .job_status import JobStatus, ALLOWED_TRANSITIONS


class Job:
    def __init__(
            self,
            id: str,
            product_id: str,
            dataset: JobDataset,
            metadata: dict,
            properties: dict,
            data_directory: str,
            status: JobStatus,
            created_at: datetime,
            last_accessed: datetime,
            downloaded_files: Optional[list[str]] = None,
            processed_files: Optional[list[str]] = None,
            fail_reason: Optional[str] = None
    ):
        self.id: str = id

        self.product_id: str = product_id
        self.dataset: JobDataset = dataset

        self.metadata: dict = metadata
        self.properties: dict = properties

        self.data_directory: str = data_directory

        self.status: JobStatus = status

        self.created_at: datetime = created_at
        self.last_accessed: datetime = last_accessed

        self.downloaded_files: Optional[list[str]] = downloaded_files
        self.processed_files: Optional[list[str]] = processed_files
        self.fail_reason: Optional[str] = fail_reason

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
        if to_status not in ALLOWED_TRANSITIONS[self.status]:
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

    # ------------------------------------------------
    # creation
    # ------------------------------------------------

    @classmethod
    def create(
            cls,
            dataset: JobDataset,
            metadata: dict,
            properties: dict,
            data_directory: str
    ) -> "Job":

        now = datetime.now(timezone.utc)

        job_id = str(uuid.uuid4())  # TODO možná by to spíš mělo být metadata[dataset.product_id_key()]
        product_id = metadata[dataset.product_id_key()]

        data_directory: str = os.path.join(data_directory, job_id, "data")

        return cls(
            id=job_id,
            product_id=product_id,
            dataset=dataset,
            metadata=metadata,
            properties=properties,
            data_directory=data_directory,
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

        return {
            "_id": self.id,
            "product_id": self.product_id,
            "dataset": self.dataset.value,
            "metadata": self.metadata,
            "properties": self.properties,
            "data_directory": self.data_directory,
            "status": self.status.value,
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "downloaded_files": self.downloaded_files,
            "processed_files": self.processed_files,
            "fail_reason": self.fail_reason,
        }

    @classmethod
    def deserialize(cls, doc: dict) -> "Job":
        return cls(
            id=doc["_id"],
            product_id=doc["product_id"],
            dataset=JobDataset(doc["dataset"]),
            metadata=doc["metadata"],
            properties=doc["properties"],
            data_directory=doc["data_directory"],
            status=JobStatus(doc["status"]),
            created_at=doc["created_at"],
            last_accessed=doc["last_accessed"],
            downloaded_files=doc.get("downloaded_files"),
            processed_files=doc.get("processed_files"),
            fail_reason=doc.get("fail_reason"),
        )
