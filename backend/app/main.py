import uuid

from fastapi import FastAPI

from .application.orchestrators import BaseOrchestrator, CeleryOrchestrator
from .domain import JobRepository
from .infrastructure.db import MongoJobRepository
from .infrastructure.logging.logger import configure_logging

configure_logging()

app = FastAPI(title="Oculus - GJTIFF wrapper service")
repo: JobRepository = MongoJobRepository()
orchestrator: BaseOrchestrator = CeleryOrchestrator()


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    repo.create(job_id)
    orchestrator.run_pipeline(job_id)
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    return repo.get(job_id)
