from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.api.v1.schemas.events_schema import EventCreateRequest, EventUpdateRequest
from app.application.events.use_cases import CreateEventUseCase
from app.application.use_cases.entity_use_cases import EventUseCases
from app.domain.events.entities import Event
from app.domain.events.services import EventService
from tests.utils import generate_random_string

event_data = {
    "title": "Concert",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime.now(UTC) + timedelta(weeks=6),
    "capacity": 5,
}


@pytest.fixture(scope="function")
def override_event_uc(wrap_uc_with_test_session):
    return wrap_uc_with_test_session(EventUseCases)


class TestGroupEventUseCases:
    async def test_created_event_use_case_calls_repo(self):
        repo = AsyncMock()
        service = EventService(repo)
        uc = CreateEventUseCase(service)

        req_event_data = EventCreateRequest(**event_data)
        await uc.execute(req_event_data)

        repo.create.assert_called_once()

    async def test_created_event_use_case(self, override_event_uc):
        async with EventUseCases.create_event() as use_case:
            req_event_data = EventCreateRequest(**event_data)
            result = await use_case.execute(req_event_data)

            assert isinstance(result, Event)
            assert result.id is not None

    async def test_get_event_use_case(self, override_event_uc):
        async with EventUseCases.get_event() as use_case:
            event_id = 1  # The recently added as above
            result = await use_case.execute(event_id)

            assert result.id == event_id
            assert isinstance(result, Event)

    async def test_get_not_existing_event_use_case_(self, override_event_uc):
        async with EventUseCases.get_event() as use_case:
            event_id = 99
            with pytest.raises(HTTPException):
                await use_case.execute(event_id)

    async def test_list_events_use_case(self, override_event_uc):
        async with EventUseCases.list_events() as use_case:
            result: dict = await use_case.execute()

            assert result["total"] == 1
            assert isinstance(result["items"][0], Event)
            # Parameters are default
            assert result["page"] == 1
            assert result["page_size"] == 10

    async def test_update_event_use_case_(self, override_event_uc):
        async with EventUseCases.update_event() as use_case:
            event_id = 1
            event_data = EventUpdateRequest(
                description=f"New description {generate_random_string()}"
            )
            result: Event = await use_case.execute(event_id, event_data)

            assert result.description == event_data.description
            assert abs(result.updated_at - datetime.now(UTC)) < timedelta(seconds=5)
