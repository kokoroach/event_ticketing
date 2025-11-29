from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    title: str
    description: str
    event_type: str
    venue: str
    capacity: int
    start_time: datetime
    created_at: datetime
    updated_at: datetime

    def __repr__(self) -> str:
        return (
            f"Event(id={self.id!r}, "
            f"title={self.title!r}, "
            f"event_type={self.event_type!r})"
        )
