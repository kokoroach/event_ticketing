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
