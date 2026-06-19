import logging
import os
import time
from abc import ABC, abstractmethod
from typing import Optional

from ...domain import Job, FeatureState
from ...settings import settings


class Processor(ABC):

    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger: Optional[logging.Logger] = None
    ):
        self._job = job
        self._feature_state = feature_state

        self._logger = logger or logging.getLogger(settings.APP_NAME)

        self._path_to_processed = os.path.join(
            str(self._feature_state.feature_root_directory),
            "processed"
        )

    def get_files_to_process(self) -> list[str]:
        files_to_process: list[str] = []

        for filename in self._job.requested_files:

            file_state = self._feature_state.get_file_state(filename)

            if file_state is None:
                raise ValueError(f"File {filename} is expected but it does not exist at all.")

            if not file_state.is_downloaded:
                raise ValueError(f"File {filename} is expected to be downloaded, but it is not.")

            if file_state.is_processed:
                continue

            files_to_process.append(str(file_state.download_path))

        return files_to_process

    def process(
            self,
            files_to_process: list[str]
    ) -> list[str]:

        self._logger.info(f"Processing job {self._job.id}")

        self._input_files = files_to_process

        self._ensure_output_dir()

        start = time.perf_counter()

        processed_files: list[str] = self._process()

        end = time.perf_counter()

        self._logger.info(f"Processed {len(processed_files)} files in {(end - start):.3f}")

        return processed_files

    @abstractmethod
    def _process(self) -> list[str]:
        ...

    def _ensure_output_dir(self):
        os.makedirs(
            self._path_to_processed,
            exist_ok=True
        )

    def _validate_int_param(
            self,
            value,
            default,
            param_name: str = "*name_unspecified*"
    ):
        if value is None:
            return default

        try:
            return int(value)

        except (ValueError, TypeError):

            self._logger.warning(
                f"Invalid {param_name}: {value}. "
                f"Using default {default}"
            )

            return default

    def _validate_zoom_levels(
            self,
            zoom_levels,
            default_zoom_levels: list[int]
    ) -> list[int]:

        # TODO tady bude asi spíš něco ve smyslu _compute_zoom_levels
        # Budou se počítat podle rozlišení snímku a oblasti, kterou pokrývá

        """
        Validate zoom levels: if any value invalid, use default. Fill missing values between min..max.
        """

        if zoom_levels is None:
            zoom_levels = default_zoom_levels

        else:
            try:
                zoom_levels = [int(zoom_level) for zoom_level in zoom_levels]

            except (ValueError, TypeError):

                self._logger.warning(
                    f"Invalid zoom levels entered: {zoom_levels}. "
                    f"Defaulting to {default_zoom_levels[0]}..{default_zoom_levels[-1]}"
                )

                zoom_levels = default_zoom_levels

        zoom_min = min(zoom_levels)
        zoom_max = max(zoom_levels)

        zoom_levels = list(range(zoom_min, zoom_max + 1))

        return zoom_levels
