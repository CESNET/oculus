import re

from .sentinel_downloader import SentinelDownloader
from ...domain import Job


class Sentinel1Downloader(SentinelDownloader):
    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

    def _filter_files(self, available_files: list[str] = None) -> list[str]:
        if not available_files:
            return []

        filtered_files = []

        requested_polarizations = set(
            self._job.properties.get("filters", {}).get(
                "polarisation_channels", ["VV", "VH", "HH", "HV"]  # default all polarizations
            )
        )

        for file in available_files:
            file_strip_lower = file.strip().lower()

            # only measurement TIFFs
            if "/measurement/" not in file_strip_lower or not re.search(r"\.(tif|tiff)$", file_strip_lower):
                continue

            # loose filter
            matched = False
            for pol in requested_polarizations:
                if f"-{pol.lower()}-" in file_strip_lower:
                    matched = True

            if matched:
                filtered_files.append(file)

        return filtered_files
