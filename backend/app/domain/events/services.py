from app.application.uow import SQLAlchemyUnitOfWork as _UnitOfWork
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository

from .entities import Event


class EventService:

    @staticmethod
    def _repo(uow: _UnitOfWork) -> SqlAlchemyEventRepository:
        return uow.get_repo(SqlAlchemyEventRepository)

    async def create_event(self, uow: _UnitOfWork, data: Event) -> Event:
        return await self._repo(uow).create(data)

    async def get_event(self, uow: _UnitOfWork, event_id: int) -> Event | None:
        return await self._repo(uow).get(event_id)

    async def list_events(self, uow: _UnitOfWork) -> list[Event]:
        return await self._repo(uow).all()
