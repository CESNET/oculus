import json
import time
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..bootstrap_container import bootstrap_container
from ..domain import JobStatus, FAILED_STATUSES

jobs_router = APIRouter()


class CreateJobRequestModel(BaseModel):
    dataset: str
    metadata: dict
    properties: dict


@jobs_router.post("/create")
def create_job(request: CreateJobRequestModel):
    job_id = bootstrap_container.create_job().execute(
        dataset=request.dataset,
        metadata=request.metadata,
        properties=request.properties
    )
    return {"job_id": job_id}


@jobs_router.get("/{job_id}")
def get_job(job_id: str):
    return bootstrap_container.repository.get(job_id).serialize()


@jobs_router.get("/{job_id}/events")
def stream_job_events(job_id: str):
    return StreamingResponse(
        _job_event_generator(job_id),
        media_type="text/event-stream"
    )


# ------------------------------------------------
# Helpers
# ------------------------------------------------

def _job_event_generator(job_id: str, heartbeat_interval: float = 15.0):
    subscribe_client = bootstrap_container.redis_pubsub.subscribe(job_id=job_id)

    try:
        job = bootstrap_container.repository.get(job_id)
        last_status = job.status
        yield f"data: {json.dumps({'status': last_status, 'timestamp': job.last_accessed.isoformat()})}\n\n"

        if last_status in FAILED_STATUSES or last_status == JobStatus.FINISHED:
            return

        last_heartbeat = time.time()

        while True:
            message = subscribe_client.get_message(timeout=1.0)
            if message and message["type"] == "message":
                data = message["data"]
                last_status = data
                yield f"data: {json.dumps({'status': data, 'timestamp': datetime.now(timezone.utc).isoformat()})}\n\n"

                if last_status in FAILED_STATUSES or last_status == JobStatus.FINISHED:
                    break

            if (time.time() - last_heartbeat) > heartbeat_interval:
                job = bootstrap_container.repository.get(job_id)

                if job.status != last_status:
                    last_status = job.status
                    yield f"data: {json.dumps({'status': job.status, 'timestamp': job.last_accessed.isoformat()})}\n\n"

                else:
                    yield ":\n\n"

                last_heartbeat = time.time()

            time.sleep(0.1)

    finally:
        subscribe_client.close()
