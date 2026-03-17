from fastapi import APIRouter
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
    return bootstrap_container.repository.get(job_id).serialize()


@jobs_router.get("/{job_id}/events")
def stream_job_events(job_id: str):
    return StreamingResponse(
        job_event_generator(job_id),
        media_type="text/event-stream"
    )
