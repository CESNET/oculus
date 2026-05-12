from pymongo import MongoClient

from ...settings import settings

_mongo_client = None


def get_database():
    global _mongo_client

    if _mongo_client is None:
        _mongo_client = MongoClient(settings.MONGO_URI)

    return _mongo_client[settings.MONGO_DATABASE]


def get_collection(collection_name: str):
    db = get_database()
    return db[collection_name]
