import random
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.exc import IntegrityError

from app.api.v1.schemas.events_schema import EventCreateRequest
from app.core.config import settings
from app.infrastructure.db.models.event_model import EventModel
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from tests.utils import get_non_nullable_fields, is_timezone_aware

event_data = {
    "title": "Concert",
    "description": "Live",
    "event_type": "concert",
    "venue": "Cebu City",
    "capacity": 20,
    "start_time": datetime.now(UTC) + timedelta(weeks=5),
}


async def test_event_repo_create(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)

    data = EventCreateRequest(**event_data).model_dump(exclude_unset=True)
    result = await repo.create(data)

    # Static checks
    for key in data:
        assert getattr(result, key) == data[key]

    # Dynamic checks
    assert result.id is not None

    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)

    assert is_timezone_aware(result.created_at)
    assert is_timezone_aware(result.updated_at)

    assert result.updated_at.tzinfo == settings.DEFAULT_TIMEZONE


async def test_event_repo_create_with_missing_not_nullable_field(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)

    event = EventCreateRequest(**event_data)

    not_null_fields = get_non_nullable_fields(
        EventModel, except_for=["id", "created_at", "updated_at"]
    )
    column = random.choice(not_null_fields)

    # Override not nullable field
    setattr(event, column, None)
    with pytest.raises(IntegrityError):
        await repo.create(event.model_dump())
