import logging
import os
from abc import ABC, abstractmethod
from typing import Optional
import time

from ...domain import Job
from ...settings import settings


class Processor(ABC):
    def __init__(self, job: Job, logger: Optional[logging.Logger] = None):
        self._job = job
        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)
        self._path_to_processed = os.path.join(settings.DATA_DIR, self._job.id, "data", "processed")

    def process(self) -> list[str]:
        self._logger.info(f"Processing job {self._job.id}")

        self._ensure_input_files()
        self._ensure_output_dir()

        start = time.perf_counter()

        processed_files: list[str] = self._process()

        end = time.perf_counter()

        self._logger.debug(f"Processed {len(processed_files)} files in {end - start}")

        return processed_files

    @abstractmethod
    def _process(self) -> list[str]:
        ...

    # -------------------------------
    # Helper methods
    # -------------------------------
    def _ensure_input_files(self):
        input_files = getattr(self._job, "downloaded_files", [])
        if not input_files:
            raise ValueError("No input files specified!")
        self._input_files = input_files

    def _ensure_output_dir(self):
        os.makedirs(self._path_to_processed, exist_ok=True)

    def _validate_int_param(self, value, default, param_name: str = "*name_unspecified*"):
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            self._logger.warning(f"Invalid {param_name}: {value}. Using default {default}")
            return default

    def _validate_zoom_levels(self, zoom_levels, default_zoom_levels: list[int]) -> list[int]:
        """
        Validate zoom levels: if any value invalid, use default. Fill missing values between min..max.
        """
        if zoom_levels is None:
            zoom_levels = default_zoom_levels
        else:
            try:
                zoom_levels = [int(z) for z in zoom_levels]
            except (ValueError, TypeError):
                self._logger.warning(
                    f"Invalid zoom levels entered: {zoom_levels}. Defaulting to {default_zoom_levels[0]}..{default_zoom_levels[-1]}"
                )
                zoom_levels = default_zoom_levels

        zoom_min, zoom_max = min(zoom_levels), max(zoom_levels)
        zoom_levels = list(range(zoom_min, zoom_max + 1))

        return zoom_levels
