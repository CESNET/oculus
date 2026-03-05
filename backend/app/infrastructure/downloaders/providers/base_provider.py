import logging
import os
from abc import ABC, abstractmethod

from ....config import APP_NAME, DATA_DIR
from ....domain import Job


class BaseProvider(ABC):
    def __init__(
            self,
            job: Job,
            logger: logging.Logger | None = None
    ):
        self._logger = logger or logging.getLogger(APP_NAME)

        self._job = job

        self._path_to_downloaded = os.path.join(DATA_DIR, self._job.id, "data", "downloaded")

    @abstractmethod
    def has_product(self) -> bool:
        pass

    @abstractmethod
    def get_available_files(self)->list[str]:
        pass

    @abstractmethod
    def download_product(self) -> str:
        pass
