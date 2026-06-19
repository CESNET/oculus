from contextlib import AbstractContextManager
from typing import Protocol
from enum import Enum

from .feature_state import FeatureStateId


class FeatureStateLockType(str, Enum):
    DOWNLOADING = "DOWNLOADING"
    PROCESSING = "PROCESSING"

class FeatureStateLockRepository(Protocol):

    def lock(
            self,
            feature_state_id: FeatureStateId,
            lock_type: FeatureStateLockType,
            timeout: int = 3600,
    ) -> AbstractContextManager:
        ...
