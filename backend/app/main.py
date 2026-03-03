from fastapi import FastAPI

from .api.jobs import api_router
from .infrastructure.logging.logger import configure_logging

configure_logging()

app = FastAPI(title="Oculus - GJTIFF wrapper service")
app.include_router(api_router, prefix="/jobs", tags=["jobs"])
