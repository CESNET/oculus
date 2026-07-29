import logging
from typing import Optional

from . import DownloadService
from .providers import USGSProvider
from ...domain import Job, FeatureState


class LandsatDownloadService(DownloadService):
    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger: Optional[logging.Logger] = None
    ):
        super().__init__(
            job=job,
            feature_state=feature_state,
            logger=logger
        )

        self._providers = [
            USGSProvider(
                feature_id=job.feature_id,
                feature_root_directory=feature_state.feature_root_directory,
            )
        ]

    def _filter_files(self, available_files: list[str]) -> list[str]:
        raise NotImplementedError("Files filtering is not implemented for Landsat!")
