from abc import abstractmethod

from .feature_state import FeatureState, FeatureStateId
from ..common.base_repository import BaseRepository


class FeatureStateRepository(BaseRepository[FeatureState]):

    def get_by_dataset(self, dataset: str, feature_id: str) -> FeatureState:
        entity_id = FeatureStateId.from_parts(dataset, feature_id)
        return self.get(entity_id)

    @abstractmethod
    def get(self, entity_id: FeatureStateId) -> FeatureState:
        pass

    @abstractmethod
    def save(self, entity: FeatureState):
        pass

    @abstractmethod
    def find_expired(self, threshold):
        pass

    @abstractmethod
    def delete(self, entity_id: FeatureStateId):
        pass
