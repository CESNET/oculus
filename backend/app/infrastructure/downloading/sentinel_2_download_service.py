import re
from typing import Optional

from ...domain.visualization import filter_sentinel2_files
from .sentinel_download_service import SentinelDownloadService
from ...domain import Job, FeatureState


class Sentinel2DownloadService(SentinelDownloadService):
    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger=None
    ):
        super().__init__(
            job=job,
            feature_state=feature_state,
            logger=logger
        )

    def _filter_files(self, available_files: Optional[list[str]] = None) -> list[str]:
        if available_files is None:
            return []

        filtered_files: list[str] = []

        # selected_bands_pattern = "|".join(self._get_selected_bands())
        extensions = ['jp2', 'j2k', 'jpf', 'jpm', 'jpg2', 'j2c', 'jpc', 'jpx', 'mj2']
        extensions_pattern = "|".join(extensions)
        regex_pattern = rf"(?:.*/)?(?!.*MSK)(?!.*_PVI\.)[^/]+\.({extensions_pattern})$"  # anything ending with correct extension and not being a mask file (MSK) or PVI file
        # csde_regex_pattern = rf"([^/]+)/GRANULE/([^/]+)/IMG_DATA/(?:R\d{{2}}m/)?([^/]+_({selected_bands_pattern})(?:_\d{{2}}m)?\.({extensions_pattern}))"

        for available_file in available_files:
            if re.match(regex_pattern, available_file.strip()):
                filtered_files.append(available_file)

        filtered_files = self._prune_low_resolution_files(files=filtered_files)

        visualizations = self._job.request_properties.get(
            "visualizations",
            {}
        )

        filtered_files = filter_sentinel2_files(
            files=filtered_files,
            visualizations=visualizations,
        )

        return filtered_files

    def _prune_low_resolution_files(self, files: list[str]) -> list[str]:
        """
        Keep only files with the highest resolution in the list of files that have resolution.
        All other files (without resolution specification) are kept as-is.

        Returns:
            List[str]: A list containing the best resolution files for each band,
                       followed by all files that did not match the resolution format.
        """
        if not files:
            return []

        best_resolution = {}  # {"B02": (resolution, index)}
        other_files = []  # files without 5-part names

        for i, f in enumerate(files):
            filename = f.split("/")[-1]
            filename_parts = re.split(r'[_.]', filename)

            if len(filename_parts) != 5:
                other_files.append(f)  # keep files without proper resolution format
                continue

            band = filename_parts[2]
            try:
                resolution = int(filename_parts[3].replace("m", ""))
            except ValueError:
                # Fallback if resolution string is malformed
                other_files.append(f)
                continue

            # Keep the file with the lowest resolution value (e.g., 10m is better than 20m)
            if band not in best_resolution or resolution < best_resolution[band][0]:
                best_resolution[band] = (resolution, i)

        # combine best-resolution files and the others
        pruned_files = [files[i] for _, i in best_resolution.values()]
        pruned_files.extend(other_files)

        return pruned_files
