from datetime import datetime

from app.domain.events.entities import Event
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository


async def test_event_repository_create(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)

    event = Event(
        title="Concert",
        description="Live",
        event_type="concert",
        venue="Cebu City",
        capacity=20,
        start_time=datetime.now(),
    )
    result = await repo.create(event)

    assert result.id is not None
