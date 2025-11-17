from datetime import datetime

from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str
    event_type: str  # TODO: Expand to enumerable
    venue: str
    capacity: int
    start_time: datetime


class EventResponse(EventCreate):
    id: int
