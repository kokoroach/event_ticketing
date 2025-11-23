from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(Generic[T], ABC):

    @abstractmethod
    async def create(self, data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> T | None:
        raise NotImplementedError
