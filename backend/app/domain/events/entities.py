from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    id: int
    title: str
    venue: str
    start_time: datetime
    capacity: int
