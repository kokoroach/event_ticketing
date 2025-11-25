from app.api.v1.schemas.events_schema import EventCreateRequest, EventUpdateRequest
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository

from .entities import Event


class EventService:

    def __init__(self, repo: SqlAlchemyEventRepository):
        self.repo = repo

    async def create_event(self, data: EventCreateRequest) -> Event:
        create_data = data.model_dump()
        return await self.repo.create(create_data)

    async def get_event_by_id(self, event_id: int) -> Event | None:
        return await self.repo.get(event_id)

    async def list_events(self, *, offset: int, limit: int) -> tuple[list[Event], int]:
        events = await self.repo.get_paginated_events(offset=offset, limit=limit)
        total = await self.repo.count()
        return events, total

    async def update_event(self, event_id: int, data: EventUpdateRequest) -> Event:
        # Update only fields provided
        filtered_data = data.model_dump(exclude_unset=True)
        return await self.repo.update(event_id, filtered_data)
