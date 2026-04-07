from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.jobs_router import jobs_router
from .infrastructure.logging.logger import configure_logging

configure_logging()

app = FastAPI(title="Oculus - GJTIFF wrapper service")

app.add_middleware( # TODO Nastavit na produkci
    CORSMiddleware,
    allow_origins=["*"],  # povolit všechny originy
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, OPTIONS, PUT, DELETE, ...
    allow_headers=["*"],  # všechny hlavičky
)

app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
