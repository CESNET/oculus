from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..application.events import job_event_generator
from ..bootstrap_container import bootstrap_container

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
    return bootstrap_container.job_repository.get(job_id).serialize()


@jobs_router.get("/{job_id}/events")
def stream_job_events(job_id: str):
    return StreamingResponse(
        job_event_generator(job_id),
        media_type="text/event-stream"
    )


class CancelJobRequestModel(BaseModel):
    job_id: str


@jobs_router.post("/cancel")
def cancel_job(request: CancelJobRequestModel):
    job = bootstrap_container.job_repository.get(request.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status in ("FINISHED", "FAILED"):
        raise HTTPException(status_code=400, detail="Cannot cancel a finished job")

    success = bootstrap_container.cancel_job().execute(job.id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to cancel job")

    return {"job_id": job.id, "status": "CANCELLED"}
