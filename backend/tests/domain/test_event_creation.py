from datetime import UTC, datetime

import pytest

from app.domain.entities.events.entities import Event

event_data = {
    "title": "Concert",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime(2020, 1, 1, tzinfo=UTC),
    "capacity": 5,
}


def test_event_creation_with_missing_fields():
    with pytest.raises(TypeError):
        Event(**event_data)


def test_event_creation_with_extra_field():
    with pytest.raises(TypeError):
        Event(id=None, created_at=None, updated_at=None, extra=None, **event_data)


def test_event_creation():
    """
    This example sets that all required fields regardless if they are None.

    Also, that the field validation are not setup, but must be caught by appropriate
    pydantic schema (e.g. Request-Response Models)
    """
    event = Event(id=None, created_at=None, updated_at=None, **event_data)
    assert event.title == event_data["title"]
