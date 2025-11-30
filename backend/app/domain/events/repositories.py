from typing import TypeVar

from app.domain.abc.repository import Repository

from .entities import Event

T = TypeVar("T")


class EventRepository(Repository[Event]):  # noqa
    async def get_paginated_events(self, *args, **kwargs) -> list[Event]:
        raise NotImplementedError

    async def count(self) -> int:
        raise NotImplementedError
