from . import Downloader
from .landsat import LandsatDownloader
from .sentinel import SentinelDownloader
from ...domain import JobDataset


class DownloaderSelector:

    def __init__(self, dataset: JobDataset):
        self.dataset: JobDataset = dataset

    def select(self) -> type[Downloader]:
        match self.dataset:
            case JobDataset.LANDSAT:
                return LandsatDownloader

            case JobDataset.SENTINEL:
                return SentinelDownloader

            case _:
                raise ValueError("Invalid dataset")
