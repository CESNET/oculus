import logging

from . import BaseProvider
from ....domain import Job


class USGSProvider(BaseProvider):
    def __init__(
            self,
            job: Job,
            logger: logging.Logger | None = None
    ):
        super().__init__(
            job=job,
            logger=logger
        )

    def has_product(self) -> bool:
        # USGS is an authoritative provider, expecting that product exists without check, returning always True
        return True

    def download_product(self) -> str:
        # TODO implementovat stahování
        raise NotImplementedError("!!! LANDSAT NOT IMPLEMENTED YET !!!")

        return self._path_to_downloaded
