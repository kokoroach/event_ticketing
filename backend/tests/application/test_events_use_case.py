from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from tests.utils import generate_random_string

from app.api.v1.schemas.events_schema import EventCreateRequest, EventUpdateRequest
from app.application.events.use_cases import (
    CreateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    UpdateEventUseCase,
)
from app.domain.events.entities import Event
from app.domain.events.services import EventService

data = {
    "title": "Concert4444",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime.now(UTC) + timedelta(weeks=6),
    "capacity": 5,
}


@pytest.fixture(scope="function")
def event_service(test_get_event_repo):
    return EventService(repo=test_get_event_repo)


class TestGroup:
    async def test_created_event_use_case_calls_repo(self):
        repo = AsyncMock()
        service = EventService(repo)
        uc = CreateEventUseCase(service)

        req_data = EventCreateRequest(**data)
        await uc.execute(req_data)

        repo.create.assert_called_once()

    async def test_created_event_use_case(self, event_service):
        uc = CreateEventUseCase(event_service)

        req_data = EventCreateRequest(**data)
        result = await uc.execute(req_data)

        assert isinstance(result, Event)
        assert result.id is not None

    async def test_get_event_use_case(self, event_service):
        uc = GetEventUseCase(event_service)
        event_id = 1  # The recently added as above
        result = await uc.execute(event_id)

        assert result.id == event_id
        assert isinstance(result, Event)

    async def test_get_not_existing_event_use_case_(self, event_service):
        uc = GetEventUseCase(event_service)
        event_id = 99

        with pytest.raises(HTTPException):
            await uc.execute(event_id)

    async def test_list_events_use_case(self, event_service):
        uc = ListEventsUseCase(event_service)
        result: dict = await uc.execute()

        assert result["total"] == 1
        assert isinstance(result["items"][0], Event)
        # Parameters are default
        # TODO: Set page sizing in config setting
        assert result["page"] == 1
        assert result["page_size"] == 10

    async def test_update_event_use_case_(self, event_service):
        uc = UpdateEventUseCase(event_service)
        event_id = 1
        data = EventUpdateRequest(
            description=f"New description {generate_random_string()}"
        )
        result: Event = await uc.execute(event_id, data)

        assert result.description == data.description
        assert abs(result.updated_at - datetime.now(UTC)) < timedelta(seconds=5)
