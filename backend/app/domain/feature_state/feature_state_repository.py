from typing import Protocol

from .feature_state import FeatureState, FeatureStateId


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

    def get_or_create(
            self,
            dataset: str,
            feature_id: str,
            root_directory: str,
    ) -> FeatureState:
        ...
