import logging
from abc import ABC, abstractmethod

from ....config import APP_NAME


class BaseProvider(ABC):
    def __init__(
            self,
            path_to_download: str,
            logger: logging.Logger | None = None
    ):
        self._path_to_download: str = path_to_download

        self._logger = logger or logging.getLogger(APP_NAME)

    @abstractmethod
    def has_product(self, product_id: str) -> bool:
        pass

    @abstractmethod
    def download_product(self, product_id: str) -> str:
        pass
