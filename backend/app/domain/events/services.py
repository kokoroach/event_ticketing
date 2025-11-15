from .entities import Event
from .repositories import EventRepository


class EventService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    async def create_event(self, event: Event):
        return await self.repo.create(event)

    async def get_event(self, event_id: int):
        return await self.repo.get(event_id)

    async def list_events(self):
        return await self.repo.all()
