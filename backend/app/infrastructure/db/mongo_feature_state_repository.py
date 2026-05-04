from datetime import datetime, timezone

from .mongo import mongo_provider
from ...domain import FeatureState, FeatureStateId, FeatureStateRepository


class MongoFeatureRepositoryNotFoundException(Exception):
    def __init__(self, feature_state_id: str):
        super().__init__(f"Feature state {feature_state_id} not found")


class MongoFeatureStateRepository(FeatureStateRepository):
    def __init__(self):
        self.collection = mongo_provider.get_collection("products")

    def get(self, entity_id: FeatureStateId) -> FeatureState:
        doc = self.collection.find_one({"_id": entity_id})

        if not doc:
            raise MongoFeatureRepositoryNotFoundException(entity_id)

        self.collection.update_one(
            {"_id": entity_id},
            {"$set": {"last_accessed": datetime.now(timezone.utc)}}
        )

        return FeatureState.deserialize(doc)

    def save(self, feature_state: FeatureState):
        data = feature_state.serialize()
        data["last_accessed"] = datetime.now(timezone.utc)

        self.collection.update_one(
            {"_id": data["_id"]},
            {"$set": data},
            upsert=True
        )

    def find_expired(self, threshold: datetime) -> list[FeatureState]:
        docs = self.collection.find(
            {"last_accessed": {"$lt": threshold}}
        )
        return [FeatureState.deserialize(d) for d in docs]

    def delete(self, entity_id: FeatureStateId):
        self.collection.delete_one({"_id": entity_id})
