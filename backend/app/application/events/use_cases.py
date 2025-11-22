from typing import Any

from app.domain.events.entities import Event
from app.domain.events.services import EventService


class CreateEventUseCase:
    def __init__(self, service: EventService) -> None:
        self.service = service

    async def execute(self, data: dict[str, Any]) -> Event:
        event = Event(
            id=None,
            title=data["title"],
            description=data["description"],
            event_type=data["event_type"],
            venue=data["venue"],
            capacity=data["capacity"],
            start_time=data["start_time"],
        )
        return await self.service.create_event(event)
