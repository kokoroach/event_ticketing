from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository

from .entities import Event


class EventService:

    def __init__(self, repo: SqlAlchemyEventRepository):
        self.repo = repo

    async def create_event(self, data: Event) -> Event:
        return await self.repo.create(data)

    async def get_event(self, event_id: int) -> Event | None:
        return await self.repo.get(event_id)

    async def list_events(self) -> list[Event]:
        return await self.repo.all()
