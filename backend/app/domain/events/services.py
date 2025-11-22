from app.application.uow import UnitOfWork
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository

from .entities import Event


class EventService:

    @staticmethod
    def _repo(uow: UnitOfWork) -> SqlAlchemyEventRepository:
        return uow.get_repo(SqlAlchemyEventRepository)

    async def create_event(self, uow: UnitOfWork, data: Event):
        return await self._repo(uow).create(data)

    async def get_event(self, uow: UnitOfWork, event_id: int):
        return await self._repo(uow).get(event_id)

    async def list_events(self, uow: UnitOfWork):
        return await self._repo(uow).all()
