import logging
import time

from . import BaseProvider
from ....domain import Job


class CDSEProvider(BaseProvider):
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
        # CDSE is an authoritative provider, expecting that product exists without check, returning always True
        return True

    def download_product(self) -> str:
        # TODO implementovat stahování
        for i in range(5):
            self._logger.info(f"CDSE downloading {self._job.product_id}; second {i}")
            time.sleep(1)

        return self._path_to_downloaded
