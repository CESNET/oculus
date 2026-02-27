import logging
import logging.config
import sys

from ...config import APP_VERSION, LOG_LEVEL, APP_NAME


class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": f"%(asctime)s | {APP_NAME} | v{APP_VERSION} | %(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout,
            "level": LOG_LEVEL,
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
        "level": LOG_LEVEL
    },
    "filters": {
        "stdout_filter": {"()": StdoutFilter}
    },
    "loggers": {
        APP_NAME: {"handlers": [], "level": LOG_LEVEL, "propagate": True},

        # FastAPI / Uvicorn
        "uvicorn": {"handlers": [], "level": LOG_LEVEL, "propagate": True},
        "uvicorn.access": {"handlers": [], "level": LOG_LEVEL, "propagate": True},
        "uvicorn.error": {"handlers": [], "level": LOG_LEVEL, "propagate": True},

        # Celery
        "celery": {"handlers": [], "level": LOG_LEVEL, "propagate": True},
        "celery.worker": {"handlers": [], "level": LOG_LEVEL, "propagate": True},
        "celery.beat": {"handlers": [], "level": LOG_LEVEL, "propagate": True},

        # Mongo
        "pymongo": {"handlers": [], "level": LOG_LEVEL, "propagate": True},

        # Redis
        "redis": {"handlers": [], "level": LOG_LEVEL, "propagate": True},
    }
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
