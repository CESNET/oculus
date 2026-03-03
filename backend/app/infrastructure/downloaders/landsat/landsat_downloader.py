from .. import Downloader
from ..providers import USGSProvider
from ....domain import Job


class LandsatDownloader(Downloader):

    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

        self._display_id = job.metadata.get("landsat:display_id") # TODO nemá to být scene_id?

        self._usgs_provider = USGSProvider(self._downloaded_data_path)

    def _download(self) -> str:
        if self._usgs_provider.has_product(self._display_id):
            self._logger.info("Product found in USGS")
            return self._usgs_provider.download_product(self._display_id)

        raise ValueError("Product not found in USGS")
