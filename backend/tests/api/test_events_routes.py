from app.api.v1.deps import get_create_event_uc
from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository


async def test_create_event_endpoint(
    test_db_session, test_usecase_builder, test_client_with_uc
):
    repo = SqlAlchemyEventRepository(test_db_session)
    service = EventService(repo)
    uc_instance = test_usecase_builder(CreateEventUseCase, service)

    async with test_client_with_uc(get_create_event_uc, uc_instance) as client:
        resp = await client.post(
            "/api/v1/events/",
            json={
                "title": "Concert",
                "description": "Concert for a cause",
                "event_type": "concert",
                "venue": "Cebussss City",
                "capacity": 4,
                "start_time": "2025-01-01T10:00:00",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Concert"
