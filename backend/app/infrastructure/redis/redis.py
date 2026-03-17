import redis

from ...settings import settings

_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis:
    global _redis_client

    if _redis_client is None:
        _redis_client = redis.from_url(settings.REDIS_BROKER, decode_responses=True)

    return _redis_client
