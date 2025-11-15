from pydantic import BaseModel


class EventCreate(BaseModel):
    title: str
    description: str


class EventResponse(EventCreate):
    id: int
