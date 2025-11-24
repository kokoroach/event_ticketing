from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.api.v1.schemas.events_schema import EventCreateRequest

data = {
    "title": "Concert",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime.now(UTC) - timedelta(weeks=6),
    "capacity": 5,
}


def test_event_creation_using_schema_with_past_start_time():
    with pytest.raises(ValidationError):
        EventCreateRequest(**data)


def test_event_creation_using_valid_schema():
    with pytest.raises(ValidationError):
        updated_data = data
        updated_data["start_time"] = (datetime.now(UTC) + timedelta(weeks=6),)

        EventCreateRequest(**data)
