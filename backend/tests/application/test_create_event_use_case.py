from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

from app.api.v1.schemas.events_schema import EventCreateRequest
from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.entities import Event
from app.domain.events.services import EventService

data = {
    "title": "Concert",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime.now(UTC) + timedelta(weeks=6),
    "capacity": 5,
}


async def test_create_event_use_case_calls_repo():
    repo = AsyncMock()
    service = EventService(repo)
    uc = CreateEventUseCase(service)

    req_data = EventCreateRequest(**data)
    await uc.execute(req_data)

    repo.create.assert_called_once()


async def test_create_event_use_case(test_get_event_repo):
    service = EventService(repo=test_get_event_repo)
    uc = CreateEventUseCase(service)

    req_data = EventCreateRequest(**data)
    result = await uc.execute(req_data)

    assert result.id is not None
    assert isinstance(result, Event)
