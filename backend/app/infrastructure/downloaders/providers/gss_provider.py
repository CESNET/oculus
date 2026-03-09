import logging

from . import BaseProvider
from ....domain import Job
from ....settings import settings


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
        if not settings.SENTINEL_ENABLE_GSS:
            self._logger.warning("GSS datasource is not enabled!")
            return False

        # TODO implementovat lookup produktu na GSS
        return False

    def list_product_files(self) -> list[str]:
        # TODO lookup produktů na GSS
        raise NotImplementedError("GSS datasource lookup is not implemented!")

    def download_product_files(self, files_to_download: list[str]) -> list[str]:
        # TODO download prodkutů z GSS
        raise NotImplementedError("GSS datasource download is not implemented!")
