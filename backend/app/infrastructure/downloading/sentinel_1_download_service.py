import re

from .sentinel_download_service import SentinelDownloadService
from ...domain import Job, FeatureState


class Sentinel1DownloadService(SentinelDownloadService):

    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger=None,
    ):
        super().__init__(
            job=job,
            feature_state=feature_state,
            logger=logger,
        )

    def _filter_files(
            self,
            available_files: list[str],
    ) -> list[str]:
        if not available_files:
            return []

        filtered_files: list[str] = []

        requested_polarizations = set(
            self._job.request_properties.get(
                "filters",
                {},
            ).get(
                "polarisation_channels",
                ["VV", "VH", "HH", "HV"],
            )
        )

        self._logger.info(f"Available files: {available_files}")

        for file in available_files:
            file_strip_lower = file.strip().lower()

            # Only TIFF files.
            if not re.search(r"\.(tif|tiff)$", file_strip_lower):
                continue

            # Keep files matching one of the requested polarizations.
            matched = any(
                f"-{polarisation.lower()}-" in file_strip_lower
                for polarisation in requested_polarizations
            )

            if matched:
                filtered_files.append(file)

        return filtered_files
