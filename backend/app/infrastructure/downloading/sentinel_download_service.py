from abc import abstractmethod

from . import DownloadService
from .providers import GSSProvider, CDSEProvider
from ...domain import Job, FeatureState


class SentinelDownloadService(DownloadService):
    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger=None
    ):
        self._providers = [
            GSSProvider(
                feature_id=job.feature_id,
                feature_root_directory=feature_state.feature_root_directory,
            ),
            CDSEProvider(
                feature_id=job.feature_id,
                feature_root_directory=feature_state.feature_root_directory,
            ),
        ]

        super().__init__(
            job=job,
            feature_state=feature_state,
            logger=logger
        )

    @abstractmethod
    def _filter_files(self, available_files: list[str]) -> list[str]:
        ...
