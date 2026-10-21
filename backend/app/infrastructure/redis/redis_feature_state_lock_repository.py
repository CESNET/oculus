import logging
from contextlib import contextmanager

from redis import Redis

from ...domain import FeatureStateId, FeatureStateLockType, FeatureStateLockRepository, FeatureStateLockError


class RedisFeatureStateLockRepository(FeatureStateLockRepository):

    def __init__(
            self,
            redis: Redis,
            logger: logging.Logger | None = None,
    ):
        self._redis = redis

        self._logger: logging.Logger = logger or logging.getLogger(__name__)

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

            except Exception as e:
                self._logger.exception(f"Failed to release lock for feature_state: {feature_state_id}. Exception: {e}")
