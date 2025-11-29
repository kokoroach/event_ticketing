import pytest

from app.application.use_cases.entity_use_cases import EventUseCases

event = {
    "title": "Concert",
    "description": "Concert for a cause",
    "event_type": "concert",
    "venue": "Cebu City",
    "capacity": 4,
    "start_time": "2026-01-01T10:00:00Z",
}


@pytest.fixture(scope="function")
def override_event_uc(wrap_uc_with_test_session):
    return wrap_uc_with_test_session(EventUseCases)


class TestGroupEventAPI:
    async def test_create_event_endpoint(self, test_client, override_event_uc):
        resp = await test_client.post("/api/v1/events/", json=event)
        data = resp.json()

        assert resp.status_code == 201
        assert data["id"] == 1
        assert data["title"] == data["title"]

    async def test_create_event_endpoint_with_missing_field(
        self, test_client, override_event_uc
    ):
        result = await test_client.post(
            "/api/v1/events/",
            json={
                "title": "Concert",
            },
        )
        assert result.status_code == 422

    async def test_get_event_endpoint(self, test_client, override_event_uc):
        event_id = 1  # Newly create event as above
        resp = await test_client.get(f"/api/v1/events/{event_id}")
        data = resp.json()

        assert resp.status_code == 200
        assert data["title"] == data["title"]
        assert data["id"] == 1

    async def test_get_non_existing_event_endpoint(
        self, test_client, override_event_uc
    ):
        resp = await test_client.get(f"/api/v1/events/{99}")
        assert resp.status_code == 404

    async def test_update_event_endpoint_with_no_body(
        self, test_client, override_event_uc
    ):
        resp = await test_client.patch(f"/api/v1/events/{99}")
        assert resp.status_code == 422

    async def test_update_non_existing_event_endpoint(
        self, test_client, override_event_uc
    ):
        resp = await test_client.patch(f"/api/v1/events/{99}", json={})
        assert resp.status_code == 404
