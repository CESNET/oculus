import logging
import time

from .downloader import Downloader


class CDSEDownloader(Downloader):
    def __init__(self, job_id: str, logger: logging.Logger = None):
        super().__init__(job_id=job_id, logger=logger)

    def _download(self) -> str:
        for i in range(10):
            self._logger.info(f"Downloading job {self._job_id}; second {i}")
            time.sleep(1)

        return self._downloaded_data_path
