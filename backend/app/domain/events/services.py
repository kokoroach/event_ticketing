from .entities import Event
from .repositories import Repository


class EventService:

    def __init__(self, repo: Repository):
        self.repo = repo

    async def create_event(self, data: Event) -> Event:
        return await self.repo.create(data)

    async def get_event(self, event_id: int) -> Event | None:
        return await self.repo.get(event_id)
