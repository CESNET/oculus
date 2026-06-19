from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from pathlib import Path

from .job_dataset import JobDataset
from .job_status import JobStatus, can_transition
from ..feature_state import FeatureStateId


@dataclass(frozen=True, slots=True)
class JobId:
    value: str

    def __str__(self) -> str:
        return self.value

    def to_json(self) -> str:
        return str(self)

    @classmethod
    def generate(cls) -> "JobId":
        return cls(str(uuid.uuid4()))

    @classmethod
    def parse(cls, value: str) -> "JobId":
        uuid.UUID(value)
        return cls(value)


@dataclass(slots=True)
class Job:
    id: JobId

    feature_state_id: FeatureStateId
    dataset: JobDataset

    metadata: dict[str, Any]
    request_properties: dict[str, Any]

    traversed_statuses: list[JobStatus]

    created_at: datetime
    last_accessed: datetime

    fail_reasons: list[str] = field(default_factory=list)

    cancel_reason: str | None = None

    requested_files: list[str] = field(default_factory=list)

    # -------------------------
    # convenience
    # -------------------------

    @property
    def feature_id(self) -> str:
        return self.feature_state_id.feature_id

    # -------------------------
    # creation
    # -------------------------

    @classmethod
    def create(
            cls,
            dataset: JobDataset,
            metadata: dict[str, Any],
            request_properties: dict[str, Any],
            feature_state_id: Optional[FeatureStateId] = None,
    ) -> "Job":

        now = datetime.now(timezone.utc)

        if feature_state_id is None:
            feature_state_id = FeatureStateId(
                dataset=dataset.name,
                feature_id=metadata[dataset.feature_id_key_name],
            )

        return cls(
            id=JobId.generate(),
            feature_state_id=feature_state_id,
            dataset=dataset,
            metadata=metadata,
            request_properties=request_properties,
            traversed_statuses=[JobStatus.ACCEPTED],
            created_at=now,
            last_accessed=now,
        )

    # -------------------------
    # status
    # -------------------------

    @property
    def current_status(self) -> JobStatus:
        if not self.traversed_statuses:
            raise RuntimeError(f"Job {self.id} has no status")

        return self.traversed_statuses[-1]

    @property
    def last_fail_reason(self) -> str | None:
        return self.fail_reasons[-1] if self.fail_reasons else None

    # -------------------------
    # behavior
    # -------------------------

    def set_requested_files(self, requested_files: list[str]) -> None:
        self.requested_files = [Path(requested_file).stem for requested_file in requested_files]

    def get_requested_files(self) -> list[str]:
        return self.requested_files

    def _touch(self) -> None:
        self.last_accessed = datetime.now(timezone.utc)

    def transition(self, to_status: JobStatus) -> None:
        self._touch()

        if self.current_status == JobStatus.CANCELLED:
            return

        if not can_transition(self.current_status, to_status):
            raise ValueError(f"Invalid transition {self.current_status} -> {to_status}")

        self.traversed_statuses.append(to_status)

    def mark_waiting_for_download_lock(self) -> None:
        self.transition(JobStatus.WAITING_FOR_DOWNLOAD_LOCK)

    def mark_downloading(self) -> None:
        self.transition(JobStatus.DOWNLOADING)

    def mark_downloading_complete(self) -> None:
        self.transition(JobStatus.DOWNLOADING_COMPLETE)

    def mark_downloading_failed(self, reason: str) -> None:
        self.fail_reasons.append(reason)

        self.transition(JobStatus.DOWNLOADING_FAILED)

    def mark_waiting_for_processing_lock(self) -> None:
        self.transition(JobStatus.WAITING_FOR_PROCESSING_LOCK)

    def mark_processing(self) -> None:
        self.transition(JobStatus.PROCESSING)

    def mark_processing_complete(self) -> None:
        self.transition(JobStatus.PROCESSING_COMPLETE)

    def mark_processing_failed(self, reason: str) -> None:
        self.fail_reasons.append(reason)

        self.transition(JobStatus.PROCESSING_FAILED)

    def mark_finalizing(self) -> None:
        self.transition(JobStatus.FINALIZING)

    def mark_finalizing_failed(self, reason: str) -> None:
        self.fail_reasons.append(reason)

        self.transition(JobStatus.FINALIZING_FAILED)

    def mark_finished(self) -> None:
        self.transition(JobStatus.FINISHED)

    def mark_failed(self, reason: str) -> None:
        self.fail_reasons.append(reason)

        self.transition(JobStatus.FAILED)

    def mark_cancelled(self, reason: str) -> None:
        self.cancel_reason = reason

        self.transition(JobStatus.CANCELLED)

    # -------------------------
    # serialization
    # -------------------------

    def to_dict(self) -> dict:
        return {
            "feature_state_id": str(self.feature_state_id),
            "dataset": self.dataset.name,
            "metadata": self.metadata,
            "request_properties": self.request_properties,
            "traversed_statuses": [status.name for status in self.traversed_statuses],
            "created_at": self.created_at,
            "last_accessed": self.last_accessed,
            "fail_reasons": self.fail_reasons,
            "cancel_reason": self.cancel_reason,
        }

    @classmethod
    def from_dict(cls, job_id: JobId, data: dict) -> "Job":
        return cls(
            id=job_id,
            feature_state_id=FeatureStateId.parse(data["feature_state_id"]),
            dataset=JobDataset.from_str(data["dataset"]),
            metadata=data["metadata"],
            request_properties=data["request_properties"],
            traversed_statuses=[JobStatus(status) for status in data.get("traversed_statuses", [])],
            created_at=data["created_at"],
            last_accessed=data["last_accessed"],
            fail_reasons=data.get("fail_reasons", []),
            cancel_reason=data.get("cancel_reason"),
        )
