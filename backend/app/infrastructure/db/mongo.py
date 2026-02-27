from pymongo import MongoClient

from ...config import MONGO_URI, MONGO_CLIENT, MONGO_DB

_mongo_client = None


def get_collection():
    global _mongo_client

    if _mongo_client is None:
        _mongo_client = MongoClient(MONGO_URI)

    db = _mongo_client[MONGO_CLIENT]
    return db[MONGO_DB]
