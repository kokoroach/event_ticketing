from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.events.entities import Event
from app.domain.events.repositories import EventRepository
from app.infrastructure.db.models.event_model import EventModel


class SqlAlchemyEventRepository(EventRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, event: Event) -> Event:
        obj = EventModel(**event.__dict__)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return Event(**obj.__dict__)

    async def get(self, event_id: int) -> Event:
        # TODO
        obj: dict = {}
        return Event(**obj)

    async def all(self) -> list[Event]:
        events: list[Event] = []

        stmt = select(EventModel)
        result = await self.session.execute(stmt)
        events = result.scalars().all()
        for event in events:
            events.append(Event(**event.__dict__))
        return events
