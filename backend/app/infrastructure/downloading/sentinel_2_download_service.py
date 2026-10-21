import re

from .sentinel_download_service import SentinelDownloadService
from ...domain import Job, FeatureState
from ...domain.dataset.sentinel_2 import (
    Sentinel2Band,
    get_required_sentinel2_bands,
)


class Sentinel2DownloadService(SentinelDownloadService):

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

        filtered_files = self._filter_image_files(available_files)

        filtered_files = self._keep_best_resolution_per_band(files=filtered_files)

        visualizations = self._job.request_properties.get("visualizations", {})

        required_bands = get_required_sentinel2_bands(visualizations)

        if not required_bands:
            return filtered_files

        return self._filter_by_required_bands(
            files=filtered_files,
            required_bands=required_bands,
        )

    # ======================================================
    # FILE TYPE
    # ======================================================

    @staticmethod
    def _filter_image_files(
            files: list[str],
    ) -> list[str]:
        extensions = [
            "jp2",
            "j2k",
            "jpf",
            "jpm",
            "jpg2",
            "j2c",
            "jpc",
            "jpx",
            "mj2",
        ]

        extensions_pattern = "|".join(extensions)

        regex_pattern = rf"(?:.*/)?(?!.*MSK)(?!.*_PVI\.)[^/]+\.({extensions_pattern})$"

        return [
            file
            for file in files
            if re.match(regex_pattern, file.strip())
        ]

    # ======================================================
    # BAND FILTER
    # ======================================================

    @staticmethod
    def _filter_by_required_bands(
            files: list[str],
            required_bands: set[Sentinel2Band],
    ) -> list[str]:
        filtered_files: list[str] = []

        for file in files:
            filename = file.split("/")[-1]
            filename_parts = re.split(r"[_.]", filename)

            if any(
                    band.value in filename_parts
                    for band in required_bands
            ):
                filtered_files.append(file)

        return filtered_files

    # ======================================================
    # RESOLUTION
    # ======================================================

    def _keep_best_resolution_per_band(
            self,
            files: list[str],
    ) -> list[str]:
        """
        Keep only the highest-resolution file for each band.

        Files with an unrecognized filename structure are kept as-is.

        For resolution-based files, the lowest resolution value is
        considered the best resolution (e.g. 10m is better than 20m).
        """
        if not files:
            return []

        best_resolution: dict[str, tuple[int, int]] = {}
        other_files: list[str] = []

        for i, file in enumerate(files):
            filename = file.split("/")[-1]
            filename_parts = re.split(r"[_.]", filename)

            if len(filename_parts) != 5:
                other_files.append(file)
                continue

            band = filename_parts[2]

            try:
                resolution = int(filename_parts[3].replace("m", ""))
            except ValueError:
                other_files.append(file)
                continue

            if (
                    band not in best_resolution
                    or resolution < best_resolution[band][0]
            ):
                best_resolution[band] = (resolution, i,)

        pruned_files = [
            files[index]
            for _, index in best_resolution.values()
        ]

        pruned_files.extend(other_files)

        return pruned_files
