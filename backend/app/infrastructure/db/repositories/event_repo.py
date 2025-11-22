from dataclasses import asdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.events.entities import Event
from app.domain.events.repositories import EventRepository
from app.infrastructure.db.models.event_model import EventModel
from app.infrastructure.db.utils import from_orm


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event: Event) -> Event:
        obj = EventModel(**asdict(event))

        self.session.add(obj)
        await self.session.flush()  # Flush to get ID without committing
        await self.session.refresh(obj)

        return from_orm(obj, Event)

    async def get(self, event_id: int) -> Event | None:
        stmt = select(EventModel).where(EventModel.id == event_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj is None:
            return None
        return from_orm(obj, Event)

    async def all(self) -> list[Event]:
        stmt = select(EventModel)
        result = await self.session.execute(stmt)
        orm_objects = result.scalars().all()
        return [from_orm(obj, Event) for obj in orm_objects]
