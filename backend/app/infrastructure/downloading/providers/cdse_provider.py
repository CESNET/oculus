import logging
from pathlib import Path

from . import BaseProvider
from ..connectors import CDSEConnector


class CDSEProvider(BaseProvider):
    def __init__(
            self,
            feature_id: str,
            feature_root_directory: Path,
            logger: logging.Logger | None = None
    ):
        super().__init__(
            feature_id=feature_id,
            feature_root_directory=feature_root_directory,
            logger=logger
        )

        self._connector: CDSEConnector = CDSEConnector(
            feature_id=self._feature_id,
            workdir=self._feature_download_directory,
            logger=self._logger
        )

    def has_product(self) -> bool:
        # CDSE is an authoritative provider, expecting that product exists without check, -> returning always True
        return True

    def list_product_files(self) -> list[str]:
        self._logger.debug(f"Querying CDSE for product {self._feature_id}")

        available_files: list[str] = self._connector.get_available_files()

        if not available_files:
            self._logger.warning(f"No files found for product {self._feature_id}")
        else:
            self._logger.info(f"Found {len(available_files)} files for product {self._feature_id}")

        return available_files

    def _download_product_files(self, files_to_download: set[str]) -> list[str]:
        self._logger.info(f"Starting CDSE download for product {self._feature_id}")

        downloaded_files: list[str] = self._connector.download_selected_files(files_to_download=files_to_download)

        return downloaded_files
