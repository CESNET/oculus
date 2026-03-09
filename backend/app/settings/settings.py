import logging
from datetime import datetime, timezone
from typing import List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

    # ------------------------------------------------------------------
    # APP
    # ------------------------------------------------------------------

    APP_NAME: str = "oculus"

    APP_VERSION: str = (
        f"{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-dev"
    )

    # ------------------------------------------------------------------
    # LOGGING
    # ------------------------------------------------------------------

    LOG_LEVEL: str = "INFO"

    @computed_field
    @property
    def LOG_LEVEL_INT(self) -> int:
        return getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)

    # ------------------------------------------------------------------
    # DATASETS
    # ------------------------------------------------------------------

    ENABLE_SENTINEL: bool = False
    ENABLE_LANDSAT: bool = False

    @computed_field
    @property
    def ENABLED_DATASETS(self) -> List[str]:
        # WARNING - datasets must correspond to `domain/job_dataset.py` definitions!
        datasets = []

        if self.ENABLE_SENTINEL:
            datasets.append("sentinel")

        if self.ENABLE_LANDSAT:
            datasets.append("landsat")

        return datasets

    SENTINEL_ENABLE_GSS: bool = False

    SENTINEL_CDSE_CATALOG_ROOT: str = "https://catalogue.dataspace.copernicus.eu/odata/v1/"
    SENTINEL_CDSE_S3_ENDPOINT_URL: str = "https://eodata.dataspace.copernicus.eu/"
    SENTINEL_CDSE_S3_REGION_NAME: str = "default"
    SENTINEL_CDSE_S3_ACCESS_KEY: str | None = None
    SENTINEL_CDSE_S3_SECRET_KEY: str | None = None

    @computed_field
    @property
    def SENTINEL_CDSE_S3_CREDENTIALS(self) -> dict[str, str | None]:

        return {
            "aws_access_key_id": self.SENTINEL_CDSE_S3_ACCESS_KEY,
            "aws_secret_access_key": self.SENTINEL_CDSE_S3_SECRET_KEY,
            "region_name": self.SENTINEL_CDSE_S3_REGION_NAME,
            "endpoint_url": self.SENTINEL_CDSE_S3_ENDPOINT_URL
        }

    # ------------------------------------------------------------------
    # PATHS
    # ------------------------------------------------------------------

    TMP_DIR: str | None = None
    DATA_DIR: str = "/data"

    @computed_field
    @property
    def TMP_DIR_RESOLVED(self) -> str:
        if self.TMP_DIR:
            return self.TMP_DIR
        return f"/tmp/{self.APP_NAME}"

    # ------------------------------------------------------------------
    # MONGO
    # ------------------------------------------------------------------

    MONGO_URI: str = "mongodb://localhost:27017"

    MONGO_CLIENT: str | None = None
    MONGO_DB: str | None = None

    @computed_field
    @property
    def MONGO_CLIENT_RESOLVED(self) -> str:
        return self.MONGO_CLIENT or f"{self.APP_NAME}-mongouser"

    @computed_field
    @property
    def MONGO_DB_RESOLVED(self) -> str:
        return self.MONGO_DB or f"{self.APP_NAME}-jobs"

    # ------------------------------------------------------------------
    # CELERY
    # ------------------------------------------------------------------

    CELERY_MAX_CONCURRENT_PROCESS_TASKS: int = 1


settings = Settings()
