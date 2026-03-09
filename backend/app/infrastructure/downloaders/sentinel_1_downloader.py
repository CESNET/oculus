import re

from .sentinel_downloader import SentinelDownloader
from ...domain import Job


class Sentinel1Downloader(SentinelDownloader):
    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

    def _filter_files(self, available_files: list[str] = None) -> list[str]:
        raise NotImplementedError("Filtering for Sentinel 1 is not implemented")
        # TODO FIND BELOW VERSION FROM PREVIOUS OCULUS VERSION

        # TODO asi bude potřeba přidělat stažení i nějakých metadat pro zobrazení v mapě

        if available_files is None:
            available_files = []

        polarisation_filter = []
        for p in self._filters['polarisation_channels']:
            if '&' in p:
                polarisation_filter.extend(p.split('&'))
            else:
                polarisation_filter.append(p)
        polarisation_filter = list(set(polarisation_filter))

        filtered_files = []

        for available_file in available_files:
            if not (
                    re.search('/measurement/', available_file[0].strip())
            ):
                continue

            for polarisation_channel in polarisation_filter:
                if re.search(f'.+-{polarisation_channel.lower()}-.+', available_file[0].strip()):
                    if available_file[0].split('.')[-1].lower() in ['tif', 'tiff']:
                        self._filters_polarisation_channels_availability[polarisation_channel.upper()] = True
                        filtered_files.append(available_file)
                        break

        return filtered_files
