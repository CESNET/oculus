import os

from celery import Celery

from ..config import APP_NAME
from ..infrastructure.logging.logger import configure_logging

celery = Celery(
    APP_NAME,
    broker=os.getenv("CELERY_BROKER", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_BACKEND", "redis://redis:6379/0")
)

celery.autodiscover_tasks(["app.tasks"])

celery.conf.beat_schedule = {
    "hourly-cleanup": {
        "task": "backend.app.tasks.cleanup_task",
        "schedule": 3600.0,
    },
}

celery.conf.worker_hijack_root_logger = False


@celery.on_after_configure.connect
def setup_celery_logging(*args, **kwargs):
    configure_logging()
