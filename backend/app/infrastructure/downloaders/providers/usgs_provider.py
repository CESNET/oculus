import logging

from . import BaseProvider


class USGSProvider(BaseProvider):
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
        display_id = product_id  # TODO možná potřeba scene_id???

        # USGS is an authoritative provider, expecting that product exists without check, returning always True
        return True

    def download_product(self, product_id: str) -> str:
        display_id = product_id  # TODO možná potřeba scene_id???

        # TODO implementovat stahování
        raise NotImplementedError("!!! LANDSAT NOT IMPLEMENTED YET !!!")

        return self._path_to_download
