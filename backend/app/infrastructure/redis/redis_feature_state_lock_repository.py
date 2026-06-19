from contextlib import contextmanager

from redis import Redis

from ...domain import FeatureStateId, FeatureStateLockType, FeatureStateLockRepository, FeatureStateLockError


class RedisFeatureStateLockRepository(FeatureStateLockRepository):

    def __init__(
            self,
            redis: Redis,
    ):
        self._redis = redis

    @contextmanager
    def lock(
            self,
            feature_state_id: FeatureStateId,
            lock_type: FeatureStateLockType,
            timeout: int = 3600,
    ):

        lock = self._redis.lock(
            name=f"feature_state:{feature_state_id}:{lock_type.value}",
            timeout=timeout,
            blocking_timeout=0,
        )

        acquired = lock.acquire()

        if not acquired:
            raise FeatureStateLockError(f"Feature {feature_state_id} is locked.")

        try:
            yield

        finally:
            try:
                lock.release()

            except Exception:
                pass
