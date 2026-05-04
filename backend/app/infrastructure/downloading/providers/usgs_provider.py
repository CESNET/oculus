import logging
from pathlib import Path

from . import BaseProvider
from ....domain import Job


class USGSProvider(BaseProvider):
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

    def has_product(self) -> bool:
        # USGS is an authoritative provider, expecting that product exists without check, returning always True
        return True

    def list_product_files(self) -> list[str]:
        # TODO lookup produktů na USGS
        raise NotImplementedError("USGS datasource lookup is not implemented!")

    def download_product_files(self, files_to_download: list[str]) -> list[str]:
        # TODO download prodkutů z USGS
        raise NotImplementedError("USGS datasource download is not implemented!")
