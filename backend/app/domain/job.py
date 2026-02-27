import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from ..config import APP_NAME, TMP_DIR

class JobStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DOWNLOADING = "DOWNLOADING"
    DOWNLOAD_COMPLETE = "DOWNLOAD_COMPLETE"
    PROCESSING = "PROCESSING"
    PROCESSING_COMPLETE = "PROCESSING_COMPLETE"
    FINISHED = "FINISHED"


class Job(BaseModel):
    id: str
    status: JobStatus
    created_at: datetime
    data_path: Optional[str] = None
    _logger: logging.Logger = logging.getLogger(APP_NAME)

    allowed_transitions: dict[str, list[JobStatus]] = {
        JobStatus.ACCEPTED: [JobStatus.DOWNLOADING],
        JobStatus.DOWNLOADING: [JobStatus.DOWNLOAD_COMPLETE],
        JobStatus.DOWNLOAD_COMPLETE: [JobStatus.PROCESSING],
        JobStatus.PROCESSING: [JobStatus.PROCESSING_COMPLETE],
        JobStatus.PROCESSING_COMPLETE: [JobStatus.FINISHED],
        JobStatus.FINISHED: []
    }

    def transition(self, to_status: JobStatus):
        if to_status not in self.allowed_transitions[self.status]:
            raise ValueError(f"Invalid transition from {self.status} to {to_status}")
        self.status = to_status

    def download_data(self):
        self.transition(JobStatus.DOWNLOADING)

        self._logger.info("Downloading data")

        from time import sleep
        for i in range(10):
            sleep(1)
            self._logger.info(f"Downloading {self.id}; second #{i}")

        self.data_path = f"{TMP_DIR}/{self.id}/data"

        self._logger.info("Data downloaded")

        self.transition(JobStatus.DOWNLOAD_COMPLETE)

    def process_data(self):
        self.transition(JobStatus.PROCESSING)

        self._logger.info("Processing data")

        from time import sleep
        for i in range(10):
            sleep(1)
            self._logger.info(f"Processing {self.id}; second #{i}")

        self._logger.info("Data processed")

        self.transition(JobStatus.PROCESSING_COMPLETE)

    def finalize(self):
        self.transition(JobStatus.FINISHED)

    # --- SERIALIZATION ---
    def serialize(self) -> dict:
        return {
            "_id": self.id,
            "status": self.status.value,
            "created_at": self.created_at,
            "data_path": self.data_path,
            "updated_at": datetime.now(tz=timezone.utc).isoformat(),
        }

    @classmethod
    def deserialize(cls, doc: dict) -> "Job":
        return cls(
            id=doc["_id"],
            status=JobStatus(doc["status"]),
            created_at=doc["created_at"],
            data_path=doc.get("data_path")
        )
