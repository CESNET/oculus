import logging
import time

from .processor import Processor
from ...domain import Job


class GJTIFFProcessor(Processor):
    _processed_data_path: str

    def __init__(self, job: Job, logger: logging.Logger = None):
        super().__init__(job=job, logger=logger)

    def _process(self) -> str:
        # TODO tady budeš čekat na gjtiff, tady se musí napsat volání toho gjtiff fastapi wrapperu
        for i in range(10):
            self._logger.info(f"Processing job {self._job.id}; second {i}")
            time.sleep(1)

        return self._processed_data_path
