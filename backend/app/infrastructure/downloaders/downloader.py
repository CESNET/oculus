import logging
from abc import ABC, abstractmethod
from typing import Optional, List

from .providers.base_provider import BaseProvider
from ...config import APP_NAME
from ...domain.job import Job


class Downloader(ABC):
    _providers: List[BaseProvider] = []

    def __init__(self, job: Job, logger: Optional[logging.Logger] = None):
        self._logger = logger or logging.getLogger(APP_NAME)

        self._job = job

    def download(self) -> str:
        for provider in self._providers:
            if provider.has_product():
                self._logger.info(
                    f"Product {self._job.product_id} found in {provider.__class__.__name__}"
                )
                return provider.download_product()

            self._logger.info(f"Product {self._job.product_id} not found in {provider.__class__.__name__}")

        raise ValueError(f"Product {self._job.product_id} not found in any provider")
