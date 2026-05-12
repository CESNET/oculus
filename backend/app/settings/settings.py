import logging
from datetime import datetime, timezone
from typing import List, Optional
from urllib.parse import quote_plus

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    # ------------------------------------------------------------------
    # APP
    # ------------------------------------------------------------------
    APP_NAME: str = "oculus"
    APP_VERSION: str = f"{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-dev"

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
        datasets = []
        if self.ENABLE_SENTINEL:
            datasets.append("sentinel")
        if self.ENABLE_LANDSAT:
            datasets.append("landsat")
        return datasets

    # Sentinel credentials
    SENTINEL_CDSE_CATALOG_ROOT: str = "https://catalogue.dataspace.copernicus.eu/odata/v1/"
    SENTINEL_CDSE_S3_ENDPOINT_URL: str = "https://eodata.dataspace.copernicus.eu/"
    SENTINEL_CDSE_S3_REGION_NAME: str = "default"
    SENTINEL_CDSE_S3_ACCESS_KEY: Optional[str] = None
    SENTINEL_CDSE_S3_SECRET_KEY: Optional[str] = None

    # GSS credentials
    ENABLE_GSS: bool = False
    GSS_ODATA_CATALOG_ROOT: Optional[str] = None
    GSS_STAC_CATALOG_ROOT: Optional[str] = None
    GSS_CLIENT_ID: Optional[str] = None
    GSS_CLIENT_SECRET: Optional[str] = None
    GSS_TOKEN_URL: Optional[str] = None
    GSS_USERNAME: Optional[str] = None
    GSS_PASSWORD: Optional[str] = None

    @computed_field
    @property
    def SENTINEL_CDSE_S3_CREDENTIALS(self) -> dict[str, Optional[str]]:
        return {
            "aws_access_key_id": self.SENTINEL_CDSE_S3_ACCESS_KEY,
            "aws_secret_access_key": self.SENTINEL_CDSE_S3_SECRET_KEY,
            "region_name": self.SENTINEL_CDSE_S3_REGION_NAME,
            "endpoint_url": self.SENTINEL_CDSE_S3_ENDPOINT_URL,
        }

    @computed_field
    @property
    def GSS_CREDENTIALS(self) -> dict[str, Optional[str]]:
        return {
            "odata_catalog_root": self.GSS_ODATA_CATALOG_ROOT,
            "stac_catalog_root": self.GSS_STAC_CATALOG_ROOT,
            "client_id": self.GSS_CLIENT_ID,
            "token_url": self.GSS_TOKEN_URL,
            "username": self.GSS_USERNAME,
            "password": self.GSS_PASSWORD,
        }

    # ------------------------------------------------------------------
    # PATHS
    # ------------------------------------------------------------------
    TMP_DIR: Optional[str] = None
    DATA_DIR: str = "/data"

    @computed_field
    @property
    def TMP_DIR_RESOLVED(self) -> str:
        return self.TMP_DIR if self.TMP_DIR else f"/tmp/{self.APP_NAME}"

    # ------------------------------------------------------------------
    # MONGO
    # ------------------------------------------------------------------
    MONGO_HOST: str = Field(default="mongo")
    MONGO_PORT: int = Field(default=27017, ge=1, le=65535)

    MONGO_DATABASE: str
    MONGO_USERNAME: str
    MONGO_PASSWORD: str

    @computed_field
    @property
    def MONGO_URI(self) -> str:
        return (
            f"mongodb://{self.MONGO_USERNAME}:{quote_plus(self.MONGO_PASSWORD)}@"
            f"{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DATABASE}"
            f"?authSource={self.MONGO_DATABASE}"
        )

    # ------------------------------------------------------------------
    # CELERY & REDIS
    # ------------------------------------------------------------------
    CELERY_MAX_CONCURRENT_PROCESS_TASKS: int = 1

    REDIS_HOST: str = Field(default="redis")
    REDIS_PORT: int = Field(default=6379, ge=1, le=65535)
    REDIS_DB: int = Field(default=0, ge=0)
    REDIS_PASSWORD: Optional[str] = None
    REDIS_USERNAME: Optional[str] = None

    @computed_field
    @property
    def REDIS_BROKER_URL(self) -> str:
        auth = ""
        if self.REDIS_USERNAME:
            auth = self.REDIS_USERNAME
            if self.REDIS_PASSWORD:
                auth += f":{quote_plus(self.REDIS_PASSWORD)}"
            auth += "@"
        elif self.REDIS_PASSWORD:
            auth = f":{quote_plus(self.REDIS_PASSWORD)}@"

        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @computed_field
    @property
    def REDIS_BACKEND_URL(self) -> str:
        return self.REDIS_BROKER_URL

    # ------------------------------------------------------------------
    # PROCESSING
    # ------------------------------------------------------------------
    DEFAULT_PROCESSING_QUALITY: int = 80
    DEFAULT_PROCESSING_ZOOM_LEVELS: list[int] = [8, 9, 10, 11, 12, 13, 14]
    DEFAULT_PROCESSING_OUTPUT_FORMATS: dict[str, dict[str, bool]] = {
        "webp": {"product": True, "tiles": True}
    }


settings = Settings()
