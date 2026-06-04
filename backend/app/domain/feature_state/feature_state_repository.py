from typing import Protocol

from .feature_state import FeatureState, FeatureStateId


class FeatureStateRepository(Protocol):

    # -------------------------
    # READ MODEL
    # -------------------------

    def get(self, feature_state_id: FeatureStateId) -> FeatureState:
        ...

    def insert(self, feature_state: FeatureState) -> None:
        ...

    def get_or_create(
            self,
            dataset: str,
            feature_id: str,
            root_directory: str,
    ) -> FeatureState:
        ...

    # -------------------------
    # DOWNLOAD CONCURRENCY
    # -------------------------

    def reserve_download(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
            timeout_seconds: int = 3600,
    ) -> bool:
        ...

    def complete_download(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> bool:
        ...

    def release_download(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> None:
        ...

    # -------------------------
    # PROCESSING CONCURRENCY
    # -------------------------

    def reserve_processing(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
            timeout_seconds: int = 3600,
    ) -> bool:
        ...

    def complete_processing(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> bool:
        ...

    def release_processing(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> None:
        ...
