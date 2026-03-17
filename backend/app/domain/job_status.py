from enum import Enum


class JobStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DOWNLOADING = "DOWNLOADING"
    DOWNLOADING_COMPLETE = "DOWNLOAD_COMPLETE"
    DOWNLOADING_FAILED = "DOWNLOAD_FAILED"
    PROCESSING = "PROCESSING"
    PROCESSING_COMPLETE = "PROCESSING_COMPLETE"
    PROCESSING_FAILED = "PROCESSING_FAILED"
    FINALIZING = "FINALIZING"
    FINALIZING_FAILED = "FINALIZING_FAILED"
    FINISHED = "FINISHED"
    FAILED = "FAILED"


ALLOWED_TRANSITIONS: dict[JobStatus, list[JobStatus]] = {
    JobStatus.ACCEPTED: [
        JobStatus.DOWNLOADING,
        JobStatus.FAILED
    ],

    JobStatus.DOWNLOADING: [
        JobStatus.DOWNLOADING_COMPLETE,
        JobStatus.DOWNLOADING_FAILED,
        JobStatus.FAILED
    ],

    JobStatus.DOWNLOADING_COMPLETE: [
        JobStatus.PROCESSING,
        JobStatus.FAILED
    ],

    JobStatus.DOWNLOADING_FAILED: [
        JobStatus.DOWNLOADING,
        JobStatus.FAILED
    ],

    JobStatus.PROCESSING: [
        JobStatus.PROCESSING_COMPLETE,
        JobStatus.PROCESSING_FAILED,
        JobStatus.FAILED
    ],

    JobStatus.PROCESSING_COMPLETE: [
        JobStatus.FINALIZING,
        JobStatus.FAILED
    ],

    JobStatus.PROCESSING_FAILED: [
        JobStatus.PROCESSING,
        JobStatus.FAILED
    ],

    JobStatus.FINALIZING: [
        JobStatus.FINISHED,
        JobStatus.FINALIZING_FAILED,
        JobStatus.FAILED
    ],

    JobStatus.FINALIZING_FAILED: [
        JobStatus.FINALIZING,
        JobStatus.FAILED
    ],

    JobStatus.FINISHED: [],
    JobStatus.FAILED: [],
}

FAILED_STATUSES: list[JobStatus] = [
    JobStatus.DOWNLOADING_FAILED,
    JobStatus.PROCESSING_FAILED,
    JobStatus.FINALIZING_FAILED,
    JobStatus.FAILED,
]
