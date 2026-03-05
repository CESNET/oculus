import logging
import re
from pathlib import Path
from typing import List, Tuple

import httpx
from ....config import CDSE_CATALOG_ROOT, CDSE_S3_ACCESS_KEY, CDSE_S3_SECRET_KEY
from dataspace.s3_client import S3Client


class CDSEConnector:
    """
    Connector pro CDSE: komunikuje s CDSE API a S3.
    Provádí získání feature, list dostupných souborů a stahování.
    """

    def __init__(self, feature_id: str, workdir: str, logger: logging.Logger | None = None):
        self._feature_id = feature_id
        self._workdir = Path(workdir)
        self._logger = logger or logging.getLogger(__name__)
        self._feature: dict | None = None
        self._s3_client = S3Client(config=CDSE_S3_CREDENTIALS)

    # -----------------------
    # API + feature
    # -----------------------
    def _get_feature(self) -> dict:
        """Získá metadata feature z CDSE API."""
        if self._feature is not None:
            return self._feature

        endpoint = f"Products({self._feature_id})"
        response: httpx.Response = httpx.get(f"{CDSE_CATALOG_ROOT}/{endpoint}")

        self._logger.debug(f"CDSE connector calling API for feature {self._feature_id}")

        if response.status_code != 200:
            raise RuntimeError(
                f"CDSE API error: {response.status_code}, response: {response.text}"
            )

        self._feature = response.json()
        return self._feature

    def get_s3_path(self) -> str:
        """Vrací S3 bucket/key pro danou feature."""
        feature = self._get_feature()
        try:
            return feature["S3Path"]
        except KeyError:
            raise FileNotFoundError(f"Feature {self._feature_id} nemá S3Path")

    # -----------------------
    # Files
    # -----------------------
    def get_available_files(self) -> List[Tuple[str, str]]:
        """
        Vrátí seznam dostupných souborů jako tuple (friendly_name, s3_key).
        friendly_name = část S3 cesty od názvu feature.
        """
        s3_path = self.get_s3_path()
        if "/eodata/" in s3_path:
            s3_path = s3_path.replace("/eodata/", "")

        all_files = self._s3_client.get_file_list(bucket_key=s3_path)
        feature_name = self._get_feature()["Name"]

        result: List[Tuple[str, str]] = []
        for f in all_files:
            m = re.search(re.escape(feature_name), f)
            if m:
                friendly_name = f[m.start():]
            else:
                friendly_name = f
            result.append((friendly_name, f))

        return result

    # -----------------------
    # Download
    # -----------------------
    def download_selected_files(self, files: List[Tuple[str, str]]) -> List[str]:
        """
        Stáhne vybrané soubory z S3.
        files = list of tuples (friendly_name, s3_key)
        """
        downloaded: List[str] = []
        self._workdir.mkdir(parents=True, exist_ok=True)

        for _, s3_key in files:
            out_path = self._s3_client.download_file(
                bucket_key=s3_key,
                root_output_directory=str(self._workdir)
            )
            downloaded.append(str(out_path))

        return downloaded

    # -----------------------
    # Geo footprint
    # -----------------------
    def get_polygon(self) -> List[List[float]]:
        """Vrací polygon feature pro případné zpracování AOI."""
        return self._get_feature()["GeoFootprint"]["coordinates"][0]