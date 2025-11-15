from app.domain.events.entities import Event
from app.domain.events.services import EventService


class CreateEventUseCase:
    def __init__(self, service: EventService):
        self.service = service

    async def execute(self, data):
        event = Event(
            id=None,
            title=data["title"],
            description=data["description"],
            date=data["date"],
        )
        return await self.service.create_event(event)
