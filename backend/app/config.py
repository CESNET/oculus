import logging
import os
from datetime import datetime, timezone

true_statements = ["1", "true", "yes", ]

APP_NAME: str = os.getenv("APP_NAME", "oculus")
APP_VERSION: str = os.getenv("APP_VERSION", f"{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-dev")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_LEVEL: int = getattr(logging, LOG_LEVEL, logging.INFO)

USE_GSS: bool = os.getenv("USE_GSS", default="False").lower() in true_statements

TMP_DIR: str = os.getenv("TMP_DIR", f"/tmp/{APP_NAME}")
DATA_DIR: str = os.getenv("DATA_DIR", f"/data")

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_CLIENT: str = os.getenv("MONGO_CLIENT", f"{APP_NAME}-mongouser")
MONGO_DB: str = os.getenv("MONGO_DB", f"{APP_NAME}-jobs")

CELERY_MAX_CONCURRENT_PROCESS_TASKS: int = int(os.getenv("CELERY_MAX_CONCURRENT_PROCESS_TASKS", 1))
