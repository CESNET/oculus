import logging
import os
from datetime import datetime, timezone

APP_NAME = os.getenv("APP_NAME", "oculus")
APP_VERSION = os.getenv("APP_VERSION", f"{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-dev")

TMP_DIR = os.getenv("TMP_DIR", f"/tmp/{APP_NAME}")
DATA_DIR = os.getenv("DATA_DIR", f"/data")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL, logging.INFO)

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_CLIENT = os.getenv("MONGO_CLIENT", f"{APP_NAME}-mongouser")
MONGO_DB = os.getenv("MONGO_DB", f"{APP_NAME}-jobs")

CELERY_MAX_CONCURRENT_PROCESS_TASKS = int(os.getenv("CELERY_MAX_CONCURRENT_PROCESS_TASKS", 1))
