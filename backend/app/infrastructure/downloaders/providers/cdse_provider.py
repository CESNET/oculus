import logging
import time

from . import BaseProvider


class CDSEProvider(BaseProvider):

    def __init__(
            self,
            path_to_download: str,
            logger: logging.Logger | None = None
    ):
        super().__init__(
            path_to_download=path_to_download,
            logger=logger
        )

    def has_product(self, product_id: str) -> bool:
        feature_id = product_id

        # CDSE is an authoritative provider, expecting that product exists without check, returning always True
        return True

    def download_product(self, product_id: str) -> str:
        feature_id = product_id

        # TODO implementovat stahování
        for i in range(5):
            self._logger.info(f"CDSE downloading {feature_id}; second {i}")
            time.sleep(1)

        return self._path_to_download
