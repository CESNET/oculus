from datetime import datetime, timezone

from .mongo import mongo_provider
from ...domain.feature_state import FeatureState, FeatureStateRepository


class MongoFeatureRepositoryNotFoundException(Exception):
    def __init__(self, feature_state_id: str):
        self.feature_state_id = feature_state_id
        message = f"Feature state {feature_state_id} not found in DB."
        super().__init__(message)


class MongoFeatureStateRepository(FeatureStateRepository):
    def __init__(self):
        self.collection = mongo_provider.get_collection("products")

    def get(self, feature_state_id: str) -> FeatureState:
        doc = self.collection.find_one({"_id": feature_state_id})
        if not doc:
            raise MongoFeatureRepositoryNotFoundException(feature_state_id=feature_state_id)

        self.collection.update_one(
            {"_id": feature_state_id},
            {"$set": {"last_accessed": datetime.now(timezone.utc)}}
        )

        return FeatureState.deserialize(doc)

    def save(self, feature_state: FeatureState):
        data = feature_state.serialize()
        data["last_accessed"] = datetime.now(timezone.utc)

        self.collection.update_one(
            {"_id": feature_state.id},
            {"$set": data},
            upsert=True
        )

    def find_expired(self, threshold: datetime):
        return list(self.collection.find(
            {"last_accessed": {"$lt": threshold}}
        ))

    def delete(self, feature_state_id: str):
        self.collection.delete_one({"_id": feature_state_id})
