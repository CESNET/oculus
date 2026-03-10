import re

from .sentinel_downloader import SentinelDownloader
from ...domain import Job


class Sentinel2Downloader(SentinelDownloader):
    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

    def _filter_files(self, available_files: list[str] = None) -> list[str]:
        if available_files is None:
            return []

        filtered_files: list[str] = []

        # selected_bands_pattern = "|".join(self._get_selected_bands())
        extensions = ['jp2', 'j2k', 'jpf', 'jpm', 'jpg2', 'j2c', 'jpc', 'jpx', 'mj2']
        extensions_pattern = "|".join(extensions)
        regex_pattern = rf"(?:.*/)?(?!.*MSK)[^/]+\.({extensions_pattern})$"  # anything ending with correct extension and not being a mask file (MSK)
        # csde_regex_pattern = rf"([^/]+)/GRANULE/([^/]+)/IMG_DATA/(?:R\d{{2}}m/)?([^/]+_({selected_bands_pattern})(?:_\d{{2}}m)?\.({extensions_pattern}))"

        for available_file in available_files:
            if re.match(regex_pattern, available_file.strip()):
                filtered_files.append(available_file)

        filtered_files = self._prune_low_resolution_files(files=filtered_files)
        filtered_files = self._filter_requested_bands(files=filtered_files)

        return filtered_files

    def _filter_requested_bands(self, files: list[str]) -> list[str]:
        """
        Filter only requested bands
        """
        if not files:
            return []

        bands = self._job.properties.get("filters", {}).get("bands")

        if not bands:
            return files

        filtered_files: list[str] = []

        for file in files:
            filename = file.split("/")[-1]
            filename_parts = re.split(r'[_.]', filename)

            if len(filename_parts) != 5:
                filtered_files.append(file)
                continue

            band = filename_parts[2]

            if band not in bands:
                continue

            filtered_files.append(file)

        return filtered_files

    def _prune_low_resolution_files(self, files: list[str]):
        """
        Keep only files with the highest resolution in the list of files that have resolution.
        All other files (without standard resolution format) are kept as-is.
        """
        if not files:
            return []

        best_resolution = {}  # {"B02": (resolution, index)}
        other_files = []  # files without 5-part names

        for i, f in enumerate(files):
            filename = f.split("/")[-1]
            filename_parts = re.split(r'[_.]', filename)

            if len(filename_parts) != 5:
                # other_files.append(f)  # keep files without proper resolution format
                continue

            band = filename_parts[2]
            resolution = int(filename_parts[3].replace("m", ""))

            if band not in best_resolution or resolution < best_resolution[band][0]:
                best_resolution[band] = (resolution, i)

        # combine best-resolution files and the others
        pruned_files = [files[i] for r, i in best_resolution.values()]
        pruned_files.extend(other_files)
        return pruned_files
