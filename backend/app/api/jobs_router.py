from fastapi import APIRouter
from pydantic import BaseModel

from ..bootstrap_container import bootstrap_container

jobs_router = APIRouter()


class CreateJobRequestModel(BaseModel):
    dataset: str
    metadata: dict
    properties: dict


"""
{
  "dataset": "sentinel",
  "metadata": {
    "sentinel:feature_id": "df4e26df-41ad-4f65-913d-d09105498515"
  },
  "properties": {
    "output_formats": [
      "jpg", "webp"
    ],
    "platform": "SENTINEL-2",
    "filters": {
      "cloud_cover": "100",
      "levels": [
        "S2MSI2A"
      ],
      "bands": [
        "TCI", "B02", "B8A"
      ]
    }
  }
}
"""


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
