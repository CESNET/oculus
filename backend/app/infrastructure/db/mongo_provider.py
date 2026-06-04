from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class MongoProvider:

    def __init__(
            self,
            mongo_uri: str,
            database_name: str,
    ):
        self._client = MongoClient(mongo_uri)
        self._database = self._client[database_name]

    @property
    def database(self) -> Database:
        return self._database

    def collection(self, name: str) -> Collection:
        return self._database[name]

    def jobs(self) -> Collection:
        return self.collection("jobs")

    def feature_states(self) -> Collection:
        return self.collection("feature_states")
