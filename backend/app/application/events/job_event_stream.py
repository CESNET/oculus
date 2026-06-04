import json
import time
from datetime import datetime, timezone

from ...bootstrap_container import bootstrap_container
from ...domain import Job, JobStatus, FAILED_STATUSES


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_event_payload(job: Job) -> dict:
    payload = {
        "job_id": job.id,
        "current_status": job.current_status,
        "timestamp": job.last_accessed.isoformat(),
    }

    if job.current_status == JobStatus.FINISHED:
        payload["processed_files"] = job.available_processed_files
        payload["available_zoom_levels"] = job.available_zoom_levels

    if job.current_status in FAILED_STATUSES:
        payload["fail_reasons"] = job.fail_reasons

    return payload


def _format_sse(data: dict = None) -> str:
    if data is None:
        return ":\n\n"

    return f"data: {json.dumps(data)}\n\n"


def job_event_generator(job_id: str, heartbeat_interval: float = 15.0):
    subscribe_client = bootstrap_container.redis_pubsub.subscribe(job_id=job_id)

    try:
        job = bootstrap_container.job_repository.get(job_id)
        last_status = job.current_status

        yield _format_sse(_build_event_payload(job))

        if last_status in FAILED_STATUSES or last_status == JobStatus.FINISHED:
            return

        last_heartbeat = time.time()

        while True:
            message = subscribe_client.get_message(timeout=1.0)
            if message and message["type"] == "message":
                job = bootstrap_container.job_repository.get(job_id)
                last_status = job.current_status
                yield _format_sse(_build_event_payload(job))

                if last_status in FAILED_STATUSES or last_status == JobStatus.FINISHED:
                    break

            now = time.time()
            if (now - last_heartbeat) > heartbeat_interval:
                job = bootstrap_container.job_repository.get(job_id)

                if job.current_status != last_status:
                    last_status = job.current_status
                    yield _format_sse(_build_event_payload(job))
                else:
                    yield _format_sse()

                last_heartbeat = now

            time.sleep(0.1)
    finally:
        subscribe_client.close()
