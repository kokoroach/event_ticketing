from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Repository(Generic[T], ABC):  # noqa
    @abstractmethod
    def __init__(self, session: Any, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> T:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, data: dict[str, Any]) -> T:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError
