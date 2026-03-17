from pymongo import MongoClient

from ...settings import settings

_mongo_client = None


def get_collection():
    global _mongo_client

    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGO_URI)

    db = _mongo_client[settings.MONGO_CLIENT_RESOLVED]
    return db[settings.MONGO_DB_RESOLVED]
