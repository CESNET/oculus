from typing import Protocol

from .feature_state import FeatureState, FeatureStateId
from ..job import Job


class FeatureStateRepository(Protocol):

    def get(
            self,
            feature_state_id: FeatureStateId,
    ) -> FeatureState:
        ...

    def save(
            self,
            feature_state: FeatureState,
    ) -> FeatureState:
        ...

    def mark_files_downloaded(
            self,
            feature_state_id: FeatureStateId,
            downloaded_files: list[str]
    ) -> FeatureState:
        ...

    def mark_files_processed(
            self,
            feature_state_id: FeatureStateId,
            processed_files: list[str]
    ) -> FeatureState:
        ...

    def get_or_create(
            self,
            dataset: str,
            feature_id: str,
            root_directory: str,
    ) -> FeatureState:
        ...
