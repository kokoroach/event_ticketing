from datetime import UTC, datetime

import pytest

from app.domain.events.entities import Event

data = {
    "title": "Concert",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime(2020, 1, 1, tzinfo=UTC),
    "capacity": 5,
}


def test_event_creation_with_missing_fields():
    with pytest.raises(TypeError):
        Event(**data)


def test_event_creation_with_extra_field():
    with pytest.raises(TypeError):
        Event(id=None, created_at=None, updated_at=None, extra=None, **data)


def test_event_creation_including_nullable_fields():
    # NOTE: This example sets that all required fields must be present
    # regardless if they are None.
    # Also, that the field validation are not setup, but must be caught by
    # by appropriate action schema
    event = Event(id=None, created_at=None, updated_at=None, **data)
    assert event.title == data["title"]
