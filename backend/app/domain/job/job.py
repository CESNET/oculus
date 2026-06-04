from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from .job_dataset import JobDataset
from .job_status import JobStatus, can_transition


class JobId(str):

    @classmethod
    def generate(cls) -> "JobId":
        return cls(str(uuid.uuid4()))

    @classmethod
    def from_str(cls, value: str) -> "JobId":
        try:
            uuid.UUID(value)
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid JobId: {value}")


class Job:

    def __init__(
            self,
            id: JobId,
            feature_id: str,
            dataset: JobDataset,
            metadata: Dict[str, Any],
            request_properties: Dict[str, Any],
            traversed_statuses: List[JobStatus],
            created_at: datetime,
            last_accessed: datetime,
            version: int = 0,
            available_downloaded_files: Optional[List[str]] = None,
            available_processed_files: Optional[List[str]] = None,
            fail_reasons: Optional[List[str]] = None,
            cancel_reason: Optional[str] = None,
    ):
        self._id = id
        self._feature_id = feature_id
        self._dataset = dataset

        self._metadata = metadata
        self._request_properties = request_properties

        self._traversed_statuses: List[JobStatus] = [] if traversed_statuses is None else list(traversed_statuses)

        self._available_downloaded_files = (
            [] if available_downloaded_files is None
            else list(available_downloaded_files)
        )
        self._available_processed_files = (
            [] if available_processed_files is None
            else list(available_processed_files)
        )

        self._created_at = created_at
        self._last_accessed = last_accessed

        self._version = version

        self._fail_reasons = [] if fail_reasons is None else list(fail_reasons)

        self._cancel_reason = cancel_reason

    @classmethod
    def create(
            cls,
            dataset: JobDataset,
            metadata: Dict[str, Any],
            request_properties: Dict[str, Any],
    ) -> "Job":

        now = datetime.now(timezone.utc)

        feature_id = metadata[dataset.feature_id_key_name]

        return cls(
            id=JobId.generate(),
            feature_id=feature_id,
            dataset=dataset,
            metadata=metadata,
            request_properties=request_properties,
            traversed_statuses=[JobStatus.ACCEPTED],
            created_at=now,
            last_accessed=now,
            version=0
        )

    # -------------------------
    # getters
    # -------------------------

    @property
    def id(self) -> JobId:
        return self._id

    @property
    def feature_id(self) -> str:
        return self._feature_id

    @property
    def dataset(self) -> Any:
        return self._dataset

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata

    @property
    def request_properties(self) -> Dict[str, Any]:
        return self._request_properties

    @property
    def traversed_statuses(self):
        return self._traversed_statuses

    @property
    def current_status(self) -> JobStatus:
        if not self._traversed_statuses:
            self.mark_failed("Job status is undefined!")

        return self._traversed_statuses[-1]

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def last_accessed(self) -> datetime:
        return self._last_accessed

    @property
    def version(self) -> int:
        return self._version

    @property
    def fail_reasons(self) -> Optional[List[str]]:
        return self._fail_reasons

    @property
    def last_fail_reason(self) -> Optional[str]:
        if not self._fail_reasons:
            return None

        return self._fail_reasons[-1]

    @property
    def cancel_reason(self) -> Optional[str]:
        return self._cancel_reason

    @property
    def available_downloaded_files(self) -> List[str]:
        return self._available_downloaded_files

    @available_downloaded_files.setter
    def available_downloaded_files(self, value):
        self._available_downloaded_files = value

    @property
    def available_processed_files(self) -> List[str]:
        return self._available_processed_files

    # -------------------------
    # behavior
    # -------------------------

    def _touch(self) -> None:
        self._last_accessed = datetime.now(timezone.utc)

    def transition(self, to_status: JobStatus) -> None:
        self._touch()

        if self.current_status == JobStatus.CANCELLED:
            return

        if not can_transition(self.current_status, to_status):
            self.mark_failed(f"Invalid transition {self._traversed_statuses} -> {to_status}")

            raise ValueError(self.last_fail_reason)

        self._traversed_statuses.append(to_status)

    def mark_downloading(self):
        self.transition(JobStatus.DOWNLOADING)

    def mark_downloading_complete(self):
        self.transition(JobStatus.DOWNLOADING_COMPLETE)

    def mark_downloading_failed(self, reason: str):
        self._fail_reasons.append(reason)
        self.transition(JobStatus.DOWNLOADING_FAILED)

    def mark_processing(self):
        self.transition(JobStatus.PROCESSING)

    def mark_processing_complete(self):
        self.transition(JobStatus.PROCESSING_COMPLETE)

    def mark_processing_failed(self, reason: str):
        self._fail_reasons.append(reason)
        self.transition(JobStatus.PROCESSING_FAILED)

    def mark_finalizing(self):
        self.transition(JobStatus.FINALIZING)

    def mark_finalizing_failed(self, reason: str):
        self._fail_reasons.append(reason)
        self.transition(JobStatus.FINALIZING_FAILED)

    def mark_finished(self):
        self.transition(JobStatus.FINISHED)

    def mark_failed(self, reason: str):
        self._fail_reasons.append(reason)
        self.transition(JobStatus.FAILED)

    def mark_cancelled(self, reason: str):
        self._cancel_reason.append(reason)
        self.transition(JobStatus.CANCELLED)
