import logging
import logging.config
import sys

from ...settings import settings


class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": f"%(asctime)s | {settings.APP_NAME} | v{settings.APP_VERSION} | %(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
            "level": settings.LOG_LEVEL,
            "filters": ["stdout_filter"]
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stderr,
            "level": logging.ERROR
        }
    },
    "root": {
        "handlers": ["stdout", "stderr"],
        "level": settings.LOG_LEVEL
    },
    "filters": {
        "stdout_filter": {"()": StdoutFilter}
    },
    "loggers": {
        settings.APP_NAME: {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},

        # FastAPI / Uvicorn
        "uvicorn": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},
        "uvicorn.access": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},
        "uvicorn.error": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},

        # Celery
        "celery": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},
        "celery.worker": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},
        "celery.beat": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},

        # Mongo
        "pymongo": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},

        # Redis
        "redis": {"handlers": [], "level": settings.LOG_LEVEL, "propagate": True},
    }
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
