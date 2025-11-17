from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    # Required fields first
    title: str
    description: str
    event_type: str
    venue: str
    capacity: int
    start_time: datetime

    # These fields are optional on factory but will be initialized by the database
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
