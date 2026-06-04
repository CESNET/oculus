from enum import Enum


class JobStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DOWNLOADING = "DOWNLOADING"
    DOWNLOADING_COMPLETE = "DOWNLOADING_COMPLETE"
    DOWNLOADING_FAILED = "DOWNLOADING_FAILED"
    PROCESSING = "PROCESSING"
    PROCESSING_COMPLETE = "PROCESSING_COMPLETE"
    PROCESSING_FAILED = "PROCESSING_FAILED"
    FINALIZING = "FINALIZING"
    FINALIZING_FAILED = "FINALIZING_FAILED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


TERMINAL_STATUSES = {JobStatus.FINISHED, JobStatus.FAILED, JobStatus.CANCELLED}

FAILED_STATUSES = [
    JobStatus.DOWNLOADING_FAILED,
    JobStatus.PROCESSING_FAILED,
    JobStatus.FINALIZING_FAILED,
    JobStatus.FAILED,
]

ALLOWED_TRANSITIONS: dict[JobStatus, list[JobStatus]] = {
    JobStatus.ACCEPTED: [
        JobStatus.DOWNLOADING
    ],
    JobStatus.DOWNLOADING: [
        JobStatus.DOWNLOADING_COMPLETE,
        JobStatus.DOWNLOADING_FAILED
    ],
    JobStatus.DOWNLOADING_COMPLETE: [
        JobStatus.PROCESSING
    ],
    JobStatus.DOWNLOADING_FAILED: [
        JobStatus.DOWNLOADING
    ],
    JobStatus.PROCESSING: [
        JobStatus.PROCESSING_COMPLETE,
        JobStatus.PROCESSING_FAILED
    ],
    JobStatus.PROCESSING_COMPLETE: [
        JobStatus.FINALIZING
    ],
    JobStatus.PROCESSING_FAILED: [
        JobStatus.PROCESSING
    ],
    JobStatus.FINALIZING: [
        JobStatus.FINISHED,
        JobStatus.FINALIZING_FAILED
    ],
    JobStatus.FINALIZING_FAILED: [
        JobStatus.FINALIZING
    ],
    JobStatus.FINISHED: [],
    JobStatus.FAILED: [],
    JobStatus.CANCELLED: [],
}


def can_transition(from_status: JobStatus, to_status: JobStatus) -> bool:
    """
    Check if a job can transition from current to next_status.
    """

    # We can always fail or cancel
    if to_status == JobStatus.FAILED or to_status == JobStatus.CANCELLED:
        return True

    return to_status in ALLOWED_TRANSITIONS.get(from_status, [])


def is_terminal_status(status: JobStatus) -> bool:
    """
    Returns True if status is final (FINISHED, FAILED, CANCELLED)
    """
    return status in TERMINAL_STATUSES
