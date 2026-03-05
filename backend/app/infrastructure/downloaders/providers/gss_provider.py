import logging

from . import BaseProvider
from ....config import ENABLE_GSS
from ....domain import Job


class GSSProvider(BaseProvider):
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
        if not ENABLE_GSS:
            self._logger.warning("GSS datasource is not enabled!")
            return False

        # TODO implementovat lookup produktu na GSS
        return False

    def download_product(self) -> str:
        # TODO implementovat stahování do path_to_download
        return self._path_to_downloaded
