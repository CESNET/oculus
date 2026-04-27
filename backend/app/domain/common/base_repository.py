from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    def get(self, entity_id: str) -> T:
        pass

    @abstractmethod
    def save(self, entity: T):
        pass

    @abstractmethod
    def find_expired(self, threshold: datetime) -> list[T]:
        pass

    @abstractmethod
    def delete(self, entity_id: str):
        pass