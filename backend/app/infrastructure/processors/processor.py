import logging
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ...domain import Job, FeatureState, ProcessorOutput, FileState
from ...settings import settings


@dataclass(slots=True)
class ProcessingBatch:
    files: list[Path]
    outputs: dict


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

        self._input_files: ProcessingBatch | None = None
        self._input_files = self.get_files_to_process()

    def get_files_to_process(self) -> ProcessingBatch:
        demanded_formats = self._job.request_properties.get(
            "outputs",
            settings.DEFAULT_PROCESSING_OUTPUT_FORMATS,
        )

        files_to_process: list[Path] = []

        for filename in self._job.get_requested_files():

            file_state = self._feature_state.get_file_state(filename)

            if file_state is None:
                raise ValueError(f"File {filename} is expected but it does not exist at all.")

            if not file_state.is_downloaded:
                raise ValueError(f"File {filename} is expected to be downloaded, but it is not.")

            if file_state.satisfies_outputs(demanded_formats):
                print(f"File {filename} is already processed, skipping.")
                continue

            if file_state.download_path is None:
                raise ValueError(f"File {filename} is expected to have a download path, but it does not.")

            files_to_process.append(file_state.download_path)

        return ProcessingBatch(
            files=files_to_process,
            outputs=demanded_formats,
        )

    def process(self) -> list[ProcessorOutput]:
        if self._input_files is None:
            raise ValueError("No files to process.")

        self._logger.info(f"Processing job {self._job.id}, total files to process: {len(self._input_files.files)}")

        self._ensure_output_dir()

        start = time.perf_counter()

        processed_outputs: list[ProcessorOutput] = self._process()

        end = time.perf_counter()

        self._logger.info(f"Processed {len(processed_outputs)} files in {(end - start):.3f}")

        return processed_outputs

    @abstractmethod
    def _process(self) -> list[ProcessorOutput]:
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

            self._logger.warning(f"Invalid {param_name}: {value}. Using default {default}")

            return default

    def _validate_zoom_levels(
            self,
            zoom_levels,
            default_zoom_levels: list[int]
    ) -> list[int]:

        self._logger.warning(f"Overriding zoom levels. Will use default {default_zoom_levels}!")
        return default_zoom_levels

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
