import logging

from . import BaseProvider
from ..connectors.gss_connector import GSSConnector
from ....domain import Job
from ....settings import settings


class GSSProvider(BaseProvider):
    def __init__(
            self,
            job: Job,
    ):
        super().__init__(
            job=job,
            logger=logging.getLogger(__name__)
        )
        self._connector = GSSConnector(feature_id=self._job.product_id,
                                  workdir=self._path_to_downloaded)

    def has_product(self) -> bool:
        if not settings.ENABLE_GSS:
            self._logger.warning("GSS datasource is not enabled!")
            return False

        if any(not value for value in settings.GSS_CREDENTIALS.values()):
            self._logger.error("GSS credentials are not configured!")
            return False

        return self._connector.get_feature() is not None

    def list_product_files(self) -> list[str]:
        available_files: list[str] = self._connector.get_available_files()

        if not available_files:
            self._logger.warning(f"No files found for product {self._job.product_id}")
        else:
            self._logger.info(f"Found {len(available_files)} files for product {self._job.product_id}")

        return available_files

    def download_product_files(self, files_to_download: list[str]) -> list[str]:
        self._logger.info(f"Starting GSS download for product {self._job.product_id}")

        downloaded_files: list[str] = self._connector.download_selected_files(files_to_download=files_to_download)

        self._logger.info(f"Finished downloading {len(downloaded_files)} files for product {self._job.product_id}")

        return downloaded_files
