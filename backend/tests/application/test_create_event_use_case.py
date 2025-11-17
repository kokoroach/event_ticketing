from unittest.mock import AsyncMock

from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.services import EventService


async def test_create_event_use_case_calls_repo(test_usecase_builder):
    repo = AsyncMock()
    service = EventService(repo)
    uc = test_usecase_builder(CreateEventUseCase, service)

    await uc.execute(
        {
            "title": "Concert",
            "description": "Some desc",
            "event_type": "concert",
            "venue": "Cebu City",
            "capacity": 4,
            "start_time": "2025-01-01T10:00:00",
        }
    )
    repo.create.assert_called_once()
