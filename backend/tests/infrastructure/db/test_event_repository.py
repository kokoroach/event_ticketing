import random
from datetime import datetime

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from app.domain.events.entities import Event
from app.infrastructure.db.models.event_model import EventModel
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository


def _get_non_nullable_fields(model_class, except_for: list[str] | None = None):
    _except_for: set = set() if except_for is None else set(except_for)

    inspector = inspect(model_class)

    non_nullable_fields = []
    for column in inspector.mapper.columns:
        if not column.nullable and column.key not in _except_for:
            non_nullable_fields.append(column.key)
    return non_nullable_fields


async def test_event_repo_create(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)
    data = {
        "title": "Concert",
        "description": "Live",
        "event_type": "concert",
        "venue": "Cebu City",
        "capacity": 20,
        "start_time": datetime.now(),
    }
    event = Event(**data)
    result = await repo.create(event)

    # Static checks
    for key in data.keys():
        assert getattr(result, key) == data[key]

    # Dynamic checks
    # TODO: Assert timezone check for result-generated `updated_at`
    assert result.id is not None
    assert isinstance(result.updated_at, datetime)


async def test_event_repo_create_with_missing_not_nullable_field(test_db_session):
    repo = SqlAlchemyEventRepository(test_db_session)
    data = {
        "title": "Concert",
        "description": "Live",
        "event_type": "concert",
        "venue": "Cebu City",
        "capacity": 20,
        "start_time": datetime.now(),
    }
    event = Event(**data)

    not_null_fields = _get_non_nullable_fields(
        EventModel, except_for=["id", "created_at", "updated_at"]
    )
    column = random.choice(not_null_fields)

    # Override not nullable field
    setattr(event, column, None)
    with pytest.raises(IntegrityError):
        await repo.create(event)
