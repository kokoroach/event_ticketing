import pytest

from app.api.v1.deps import get_create_event_uc
from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.services import EventService


@pytest.fixture
async def get_test_client(test_client_with_deps, test_get_repo):
    service = EventService(test_get_repo)
    deps_override = [
        (get_create_event_uc, lambda: CreateEventUseCase(service)),
    ]
    async with test_client_with_deps(deps_override) as client:
        yield client


async def test_create_event_endpoint(get_test_client):
    resp = await get_test_client.post(
        "/api/v1/events/",
        json={
            "title": "Concert",
            "description": "Concert for a cause",
            "event_type": "concert",
            "venue": "Cebu City",
            "capacity": 4,
            "start_time": "2026-01-01T10:00:00Z",
        },
    )
    data = resp.json()

    assert resp.status_code == 201
    assert data["title"] == "Concert"
    assert data["id"] is not None


async def test_create_event_endpoint_with_missing_field(get_test_client):
    result = await get_test_client.post(
        "/api/v1/events/",
        json={
            "title": "Concert",
        },
    )
    assert result.status_code == 422
