from typing import Any

from fastapi import HTTPException, status

from app.api.v1.schemas.events_schema import EventCreateRequest, EventUpdateRequest
from app.domain.events.entities import Event
from app.domain.events.services import EventService


class EventUseCase:
    def __init__(self, event_service: EventService) -> None:
        self.event_service = event_service

    async def execute(self, *args, **kwargs) -> Any:
        raise NotImplementedError


class CreateEventUseCase(EventUseCase):
    async def execute(self, data: EventCreateRequest) -> Event:
        return await self.event_service.create_event(data)


class GetEventUseCase(EventUseCase):
    async def execute(self, event_id: int) -> Event:
        event = await self.event_service.get_event_by_id(event_id)
        if event is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )
        return event


class ListEventsUseCase(EventUseCase):
    async def execute(self, page: int = 1, page_size: int = 10) -> dict[str, Any]:
        offset = (page - 1) * page_size
        limit = page_size

        events, total = await self.event_service.list_events(offset=offset, limit=limit)
        return {
            "items": events,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }


class UpdateEventUseCase(EventUseCase):
    async def execute(self, event_id: int, data: EventUpdateRequest) -> Event:
        event = await self.event_service.get_event_by_id(event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )
        return await self.event_service.update_event(event_id, data)
