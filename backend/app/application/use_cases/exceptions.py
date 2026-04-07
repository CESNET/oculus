from ...domain import JobStatus


class CheckJobUseCaseFailedException(Exception):
    def __init__(self, job_id: str, status: JobStatus, fail_reason: str | None = None):
        self.job_id = job_id
        self.status = status
        self.fail_reason = fail_reason
        message = f"Job {job_id} failed. Status: {status}. Reason: {fail_reason}"
        super().__init__(message)

class CheckJobUseCaseCancelledException(Exception):
    def __init__(self, job_id: str, status: JobStatus, cancel_reason: str | None = None):
        self.job_id = job_id
        self.status = status
        self.cancel_reason = cancel_reason
        message = f"Job {job_id} has been cancelled. Reason: {cancel_reason}"
        super().__init__(message)