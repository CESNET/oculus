from fastapi import FastAPI

from .api.jobs_router import jobs_router
from .infrastructure.logging.logger import configure_logging

configure_logging()

app = FastAPI(title="Oculus - GJTIFF wrapper service")
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
