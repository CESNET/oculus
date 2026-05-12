from celery import Celery

from ..logging.logger import configure_logging
from ...settings import settings

celery = Celery(
    settings.APP_NAME,
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL
)

celery.autodiscover_tasks(["app.infrastructure.celery.tasks"])

celery.conf.beat_schedule = {
    "hourly-cleanup": {
        "task": "app.infrastructure.celery.tasks.cleanup_task",
        "schedule": 3600.0,
    },
}

celery.conf.worker_hijack_root_logger = False


@celery.on_after_configure.connect
def setup_celery_logging(*args, **kwargs):
    configure_logging()
