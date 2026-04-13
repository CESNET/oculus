import requests
import logging
from pathlib import Path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .token_manager import TokenManager
from ....settings import settings


class GSSConnector:
    """
    GSS Connector: interacts with the GSS APIs.
    """

    def __init__(self, feature_id: str, workdir: str):
        self._feature_id: str = feature_id
        self._workdir: Path = Path(workdir)
        self._logger = logging.getLogger(__name__)
        self._feature: dict | None = None
        self._cached_files: list[str] | None = None

        self._token_manager = TokenManager(
            token_url=settings.GSS_TOKEN_URL,
            username=settings.GSS_USERNAME,
            password=settings.GSS_PASSWORD,
            client_id=settings.GSS_CLIENT_ID)

        self._logger.debug(f"Initialized GSS connector for feature {self._feature_id}")

        self._collections_map = { # this is temporary fix, until GSS STAC learns itself to search by ID
            "S1": "SENTINEL-1",
            "S2": "SENTINEL-2",
            "S3": "SENTINEL-3",
            "S5P": "SENTINEL-5P"
        }

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429],
            backoff_factor=2
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._http = requests.Session()
        self._http.mount("https://", adapter)

    # -----------------------
    # Feature API
    # -----------------------
    def get_feature(self) -> dict:
        if self._feature is None:
            url = f"{settings.GSS_ODATA_CATALOG_ROOT.rstrip('/')}/Products({self._feature_id})"
            self._logger.debug(f"Querying GSS Odata for product {self._feature_id} from API: {url}")

            response = self._http.get(url,
                                 headers={"Authorization": f"Bearer {self._token_manager.get_token()}"}
                                 )

            if response.status_code == 400 or response.status_code == 404: # Feature not found in GSS
                self._logger.debug(f"Feature {self._feature_id} not found in GSS")
                return None
            elif response.status_code != 200:
                self._logger.error(f"GSS API returned {response.status_code}: {response.text}")
                return None

            self._feature = response.json()
            self._logger.debug(f"Feature metadata fetched successfully for {self._feature_id}")

        self._logger.debug(f"Feature metadata fetched successfully for {self._feature}")
        return self._feature

    def get_available_files(self) -> list[str]:
        if not self._feature:
            self.get_feature()

        product_name = self._feature["Name"]
        collection_name = next((self._collections_map[collection] for collection in self._collections_map.keys() if product_name.startswith(collection)), None)

        if collection_name is None:
            self._logger.error(f"Could not determine collection for feature {product_name}")
            raise ValueError(f"Could not determine collection for feature {product_name}")

        url = f"{settings.GSS_STAC_CATALOG_ROOT.rstrip('/')}/collections/{collection_name}/items/{product_name}"
        self._logger.debug(f"Fetching STAC metadata from API: {url}")
        response = self._http.get(url,
                             headers={"Authorization": f"Bearer {self._token_manager.get_token()}"}
                             )
        if response.status_code != 200:
            self._logger.error(f"GSS STAC API returned {response.status_code}: {response.text}")
            raise RuntimeError(f"GSS STAC API error: {response.status_code}, response: {response.text}")

        self._logger.debug(f"Fetched STAC metadata including {len(response.json()['assets'])} assets.")
        return [asset["href"] for asset in response.json()["assets"].values()]

    def download_selected_files(self, files_to_download: list[str]) -> list[str]:
        self._workdir.mkdir(parents=True, exist_ok=True)

        downloaded: list[str] = []
        self._logger.debug(f"Downloading {len(files_to_download)} files to {self._workdir}")

        for https_url in files_to_download:
            out_path = self._workdir / Path(https_url).name

            try:
                self._logger.debug(f"Downloading from {https_url}")

                response = self._http.get(
                    https_url,
                    headers={"Authorization": f"Bearer {self._token_manager.get_token()}"}
                )

                if response.status_code == 200:
                    with open(out_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                    downloaded.append(str(out_path))
                    self._logger.info(f"Downloaded {https_url} to {out_path}")
                else:
                    self._logger.error(response.headers)
                    self._logger.error(f"Failed to download {https_url}: HTTP {response.status_code}")

            except Exception as e:
                self._logger.error(f"Failed to download {https_url}: {e}")

        return downloaded
