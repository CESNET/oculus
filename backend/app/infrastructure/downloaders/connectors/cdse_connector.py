import logging
import re
from typing import List, Tuple

import httpx

from app.config import CDSE_CATALOG_ROOT, CDSE_S3_CREDENTIALS
from app.infrastructure.downloaders.s3_client import S3Client


class CDSEConnector:
    """
    Nízkourovňový klient pro komunikaci s CDSE API a S3.
    Neobsahuje žádnou business logiku.
    """

    def __init__(
        self,
        feature_id: str,
        workdir: str,
        logger: logging.Logger | None = None
    ):
        self._feature_id = feature_id
        self._workdir = workdir
        self._logger = logger or logging.getLogger(__name__)

        self._feature: dict | None = None
        self._s3_client = S3Client(config=CDSE_S3_CREDENTIALS)

    # =========================
    # HTTP část
    # =========================

    def _fetch_feature(self) -> dict:
        if self._feature is not None:
            return self._feature

        endpoint = f"{CDSE_CATALOG_ROOT}/Products({self._feature_id})"

        self._logger.debug(f"Fetching CDSE feature {self._feature_id}")

        response = httpx.get(endpoint, timeout=60)

        if response.status_code != 200:
            raise RuntimeError(
                f"CDSE returned {response.status_code}: {response.text}"
            )

        self._feature = response.json()
        return self._feature

    # =========================
    # S3 část
    # =========================

    def _get_s3_path(self) -> str:
        feature = self._fetch_feature()

        try:
            return feature["S3Path"]
        except KeyError:
            raise RuntimeError("CDSE feature does not contain S3Path")

    def _get_asset_relative_path(self, full_path: str) -> str:
        feature = self._fetch_feature()
        name = feature.get("Name")

        if not name:
            return ""

        match = re.search(re.escape(name), full_path)
        if match:
            return full_path[match.start():]

        return ""

    def list_files(self) -> List[Tuple[str, str]]:
        """
        Vrací list tuple:
        (relative_asset_path, full_s3_path)
        """

        bucket_key = self._get_s3_path()

        if "/eodata/" in bucket_key:
            bucket_key = bucket_key.replace("/eodata/", "")

        self._logger.debug(f"Listing S3 files from {bucket_key}")

        available_files = self._s3_client.get_file_list(bucket_key=bucket_key)

        return [
            (self._get_asset_relative_path(file), file)
            for file in available_files
        ]

    def download_files(self, files: List[Tuple[str, str]]) -> List[str]:
        """
        Stáhne soubory do workdir.
        Vrací list lokálních cest.
        """

        downloaded: List[str] = []

        for _, full_s3_path in files:
            local_path = self._s3_client.download_file(
                bucket_key=full_s3_path,
                root_output_directory=self._workdir
            )

            downloaded.append(str(local_path))

        return downloaded