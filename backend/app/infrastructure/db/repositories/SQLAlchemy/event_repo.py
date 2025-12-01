from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.events.entities import Event
from app.domain.entities.events.repositories import EventRepository
from app.infrastructure.db.models.event_model import EventModel
from app.infrastructure.db.utils import from_orm


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, create_data: dict[str, Any]) -> Event:
        obj = EventModel(**create_data)

        self.session.add(obj)
        # Flush to get ID without committing
        await self.session.flush()
        await self.session.refresh(obj)

        return from_orm(obj, Event)

    async def _get(self, event_id: int) -> Event | None:
        stmt = select(EventModel).where(EventModel.id == event_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, event_id: int) -> Event | None:
        event = await self._get(event_id)
        if event is None:
            return None
        return from_orm(event, Event)

    async def get_paginated_events(self, *, offset: int, limit: int) -> list[Event]:
        stmt = select(EventModel).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        return [from_orm(event, Event) for event in rows]

    async def count(self) -> int:
        total = await self.session.execute(select(func.count(EventModel.id)))
        return total.scalar_one()

    async def update(self, event_id: int, update_data: dict[str, Any]) -> Event:
        event = await self._get(event_id)

        for key, value in update_data.items():
            setattr(event, key, value)

        await self.session.flush()
        await self.session.refresh(event)

        return from_orm(event, Event)

    async def delete(self): ...  # noqa: E704
