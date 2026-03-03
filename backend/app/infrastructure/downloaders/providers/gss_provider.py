import logging

from . import BaseProvider


class GSSProvider(BaseProvider):
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

        # TODO implementovat lookup produktu na GSS
        return False

    def download_product(self, product_id: str) -> str:
        feature_id = product_id

        # TODO implementovat stahování do path_to_download
        return self._path_to_download
