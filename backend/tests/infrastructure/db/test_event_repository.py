import random
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app.api.v1.schemas.events_schema import EventCreateRequest
from app.infrastructure.db.models.event_model import EventModel
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository


def is_timezone_aware(dt_obj: datetime):
    tz_info = dt_obj.tzinfo
    return tz_info is not None and tz_info.utcoffset(dt_obj) is not None


def get_non_nullable_fields(model_class, except_for: list[str] | None = None):
    _except_for: set = set() if except_for is None else set(except_for)

    inspector = inspect(model_class)

    non_nullable_fields = []
    for column in inspector.mapper.columns:
        if not column.nullable and column.key not in _except_for:
            non_nullable_fields.append(column.key)
    return non_nullable_fields


data = {
    "title": "Concert",
    "description": "Live",
    "event_type": "concert",
    "venue": "Cebu City",
    "capacity": 20,
    "start_time": datetime.now(UTC) + timedelta(weeks=5),
}


async def test_event_repo_create(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)

    event = EventCreateRequest(**data)
    result = await repo.create(event.model_dump())

    # Static checks
    for key in data.keys():
        assert getattr(result, key) == data[key]

    # Dynamic checks
    assert result.id is not None

    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)

    assert is_timezone_aware(result.created_at)
    assert is_timezone_aware(result.updated_at)


async def test_event_repo_create_with_missing_not_nullable_field(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)

    event = EventCreateRequest(**data)

    not_null_fields = get_non_nullable_fields(
        EventModel, except_for=["id", "created_at", "updated_at"]
    )
    column = random.choice(not_null_fields)

    # Override not nullable field
    setattr(event, column, None)
    with pytest.raises(IntegrityError):
        await repo.create(event.model_dump())
