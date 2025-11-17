from datetime import UTC, datetime

from app.domain.events.entities import Event


def test_event_creation():
    event = Event(
        id=None,
        title="Concert",
        description="Some descr here.",
        event_type="concert",
        venue="Manila City",
        start_time=datetime(2025, 1, 1, tzinfo=UTC),
        capacity=5,
    )
    assert event.title == "Concert"
