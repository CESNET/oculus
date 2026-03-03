from .. import Downloader
from ..providers import CDSEProvider, GSSProvider
from ....domain import Job


class SentinelDownloader(Downloader):

    def __init__(self, job: Job, logger=None):
        super().__init__(job, logger)

        self._feature_id = job.metadata.get("sentinel:feature_id")

        self._gss_provider = GSSProvider(self._downloaded_data_path)
        self._cdse_provider = CDSEProvider(self._downloaded_data_path)

    def _download(self) -> str:
        # Try GSS
        if self._gss_provider.has_product(self._feature_id):
            self._logger.info(f"Feautre_id: {self._feature_id} found in GSS")
            return self._gss_provider.download_product(product_id=self._feature_id)

        # Fallback to CDSE
        self._logger.info(f"Feautre_id: {self._feature_id} not found in GSS. Falling back to CDSE.")
        product_path = self._cdse_provider.download_product(self._feature_id)

        return product_path
