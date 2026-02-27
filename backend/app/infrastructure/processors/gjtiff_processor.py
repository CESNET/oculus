import logging
import time

from .processor import Processor


class GJTIFFProcessor(Processor):
    _processed_data_path: str

    def __init__(self, job_id: str, logger: logging.Logger = None):
        super().__init__(job_id=job_id, logger=logger)

    def _process(self) -> str:
        for i in range(10):
            self._logger.info(f"Processing job {self._job_id}; second {i}")
            time.sleep(1)

        return self._processed_data_path
