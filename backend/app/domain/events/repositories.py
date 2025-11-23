from abc import ABC, abstractmethod

from .entities import Event


class Repository(ABC):
    @abstractmethod
    async def create(self, event: Event) -> Event:
        raise NotImplementedError

    @abstractmethod
    async def get(self, event_id: int) -> Event | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self) -> Event | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self) -> Event | None:
        raise NotImplementedError


class EventRepository(Repository): ...
