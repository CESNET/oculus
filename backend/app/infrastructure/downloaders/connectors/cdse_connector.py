import logging
import re
from pathlib import Path

import boto3
import httpx
from botocore.exceptions import ClientError

from ....settings import settings


class CDSEConnector:
    """
    CDSE Connector: interacts with the CDSE API and S3 storage.
    Provides methods to fetch feature metadata, list available files, and download them.
    """

    def __init__(self, feature_id: str, workdir: str, logger: logging.Logger | None = None):
        self._feature_id: str = feature_id
        self._workdir: Path = Path(workdir)
        self._logger: logging.Logger = logger or logging.getLogger(__name__)
        self._feature: dict | None = None
        self._cached_files: list[str] | None = None

        # boto3 client and resource for fallback
        creds = settings.SENTINEL_CDSE_S3_CREDENTIALS
        self._s3_client = boto3.client(
            service_name="s3",
            endpoint_url=creds["endpoint_url"],
            aws_access_key_id=creds["aws_access_key_id"],
            aws_secret_access_key=creds["aws_secret_access_key"],
            region_name=creds["region_name"]
        )
        self._s3_resource = boto3.resource(
            service_name="s3",
            endpoint_url=creds["endpoint_url"],
            aws_access_key_id=creds["aws_access_key_id"],
            aws_secret_access_key=creds["aws_secret_access_key"],
            region_name=creds["region_name"]
        )

        self._logger.debug(f"Initialized CDSEConnector for feature {self._feature_id}")

    # -----------------------
    # Feature API
    # -----------------------
    def _get_feature(self) -> dict:
        if self._feature is None:
            url = f"{settings.SENTINEL_CDSE_CATALOG_ROOT.rstrip('/')}/Products({self._feature_id})"

            self._logger.debug(f"Fetching feature metadata from API: {url}")

            response = httpx.get(url)

            if response.status_code != 200:
                self._logger.error(f"CDSE API returned {response.status_code}: {response.text}")

                raise RuntimeError(f"CDSE API error: {response.status_code}, response: {response.text}")

            self._feature = response.json()
            self._logger.debug(f"Feature metadata fetched successfully for {self._feature_id}")

        return self._feature

    def get_s3_path(self) -> str:
        try:
            return self._get_feature()["S3Path"]
        except KeyError:
            self._logger.error(f"Feature {self._feature_id} does not contain 'S3Path'")
            raise FileNotFoundError(f"Feature {self._feature_id} does not contain S3Path key")

    # -----------------------
    # Helpers
    # -----------------------
    def _parse_s3_path(self, s3_path: str) -> tuple[str, str]:
        s3_path = s3_path.lstrip("s3:/") if s3_path.startswith("s3://") else s3_path.lstrip("/")
        parts = s3_path.split("/", 1)
        bucket = parts[0]
        prefix = parts[1] if len(parts) > 1 else ""
        return bucket, prefix

    # -----------------------
    # File Listing
    # -----------------------
    def get_available_files(self) -> list[str]:
        if self._cached_files is not None:
            return self._cached_files

        bucket, prefix = self._parse_s3_path(self.get_s3_path())

        self._logger.debug(f"Listing files in S3 bucket '{bucket}' with prefix '{prefix}'")

        files: list[str] = []
        continuation_token = None

        while True:
            list_kwargs = {"Bucket": bucket, "Prefix": prefix}

            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = self._s3_client.list_objects_v2(**list_kwargs)
            for obj in response.get("Contents", []):
                key = obj["Key"]
                files.append(key)

            if response.get("IsTruncated"):
                continuation_token = response.get("NextContinuationToken")

            else:
                break

        self._cached_files = files

        self._logger.debug(f"Found {len(files)} files for feature {self._feature_id}")

        return files

    # -----------------------
    # File Download
    # -----------------------
    def download_selected_files(self, files_to_download: list[str]) -> list[str]:
        self._workdir.mkdir(parents=True, exist_ok=True)
        bucket, _ = self._parse_s3_path(self.get_s3_path())

        downloaded: list[str] = []
        self._logger.debug(f"Downloading {len(files_to_download)} files to {self._workdir}")

        for s3_key in files_to_download:
            out_path = self._workdir / Path(s3_key).name

            try:
                # Fallback: first try client, if fails, try resource
                try:
                    self._s3_client.download_file(bucket, s3_key, str(out_path))

                except ClientError:
                    self._logger.warning(f"Client download failed for {s3_key}, using resource fallback")

                    self._s3_resource.Object(bucket, s3_key).download_file(str(out_path))

                downloaded.append(str(out_path))
                self._logger.info(f"Downloaded {s3_key} to {out_path}")

            except ClientError as e:
                self._logger.error(f"Failed to download {s3_key}: {e}")

        return downloaded

    # -----------------------
    # Geo footprint
    # -----------------------
    def get_polygon(self) -> list[list[float]]:
        return self._get_feature()["GeoFootprint"]["coordinates"][0]
