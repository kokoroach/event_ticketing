import pytest

from app.api.v1.deps import create_event_uc
from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.services import EventService

event = {
    "title": "Concert",
    "description": "Concert for a cause",
    "event_type": "concert",
    "venue": "Cebu City",
    "capacity": 4,
    "start_time": "2026-01-01T10:00:00Z",
}


# TODO: Improve this test suite as running them in different test case raises either
#   the following:
# 1. sqlalchemy.exc.InterfaceError: (sqlalchemy.dialects.postgresql.asyncpg.InterfaceError)  # noqa E501
#   <class 'asyncpg.exceptions._base.InterfaceError'>: cannot perform operation: another operation is in progress # noqa E501
# 2. AttributeError: 'NoneType' object has no attribute 'send'
#   C:\Python312\Lib\asyncio\proactor_events.py:402: AttributeError


@pytest.fixture(scope="function")
async def test_client(test_client_with_deps, test_get_event_repo):
    """
    Returns a single AsyncClient shared by all tests in the module.
    Dependencies are injected only once.
    """
    service = EventService(test_get_event_repo)
    deps_override = [
        (create_event_uc, lambda: CreateEventUseCase(service)),
    ]

    # Run the context manager once and yield the client
    async with test_client_with_deps(deps_override) as client:
        yield client


async def test_create_event_endpoint(test_client):
    resp = await test_client.post("/api/v1/events/", json=event)
    data = resp.json()

    assert resp.status_code == 201
    assert data["id"] == 1
    assert data["title"] == data["title"]


async def test_create_event_endpoint_with_missing_field(test_client):
    result = await test_client.post(
        "/api/v1/events/",
        json={
            "title": "Concert",
        },
    )
    assert result.status_code == 422


async def test_get_event_endpoint(test_client):
    event_id = 1  # Newly create event as above
    resp = await test_client.get(f"/api/v1/events/{event_id}")
    data = resp.json()

    assert resp.status_code == 200
    assert data["title"] == data["title"]
    assert data["id"] == 1


async def test_get_non_existing_event_endpoint(test_client):
    resp = await test_client.get(f"/api/v1/events/{99}")
    assert resp.status_code == 404


async def test_update_event_endpoint_with_no_body(test_client):
    resp = await test_client.patch(f"/api/v1/events/{99}")
    assert resp.status_code == 422


async def test_update_non_existing_event_endpoint(test_client):
    resp = await test_client.patch(f"/api/v1/events/{99}", json={})
    assert resp.status_code == 404
