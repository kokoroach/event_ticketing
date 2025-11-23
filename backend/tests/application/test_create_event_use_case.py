from datetime import UTC, datetime
from unittest.mock import AsyncMock

from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.entities import Event
from app.domain.events.services import EventService


async def test_create_event_use_case_calls_repo():
    repo = AsyncMock()
    service = EventService(repo)
    uc = CreateEventUseCase(service)

    await uc.execute(
        {
            "title": "Concert",
        }
    )
    repo.create.assert_called_once()


async def test_create_event_use_case(test_get_repo):
    service = EventService(repo=test_get_repo)
    uc = CreateEventUseCase(service)

    data = Event(
        id=None,
        title="Concert",
        description="Some descr here.",
        event_type="concert",
        venue="Manila City",
        start_time=datetime(2025, 1, 1, tzinfo=UTC),
        capacity=5,
    )
    result = await uc.execute(data)

    assert result.id is not None
