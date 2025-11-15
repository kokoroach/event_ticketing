from abc import ABC, abstractmethod

from .entities import Event


class EventRepository(ABC):
    @abstractmethod
    async def create(self, event: Event) -> Event:
        raise NotImplementedError

    @abstractmethod
    async def get(self, event_id: int) -> Event | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self) -> list[Event]:
        raise NotImplementedError
