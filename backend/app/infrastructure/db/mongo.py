from pymongo import MongoClient

from ...settings import settings


class MongoProvider:
    def __init__(self):
        self._client = MongoClient(settings.MONGO_URI)

    @property
    def db(self):
        return self._client[settings.MONGO_CLIENT_RESOLVED]

    def get_collection(self, name: str):
        return self.db[name]


mongo_provider = MongoProvider()
