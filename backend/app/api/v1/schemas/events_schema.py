from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class EventBase(BaseModel):
    id: int = Field(None, description="Event ID")
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(
        ..., min_length=1, max_length=1000, description="Event description"
    )
    event_type: str = Field(
        ..., min_length=1, max_length=255, description="Type of event"
    )
    venue: str = Field(..., min_length=1, max_length=255, description="Event venue")
    capacity: int = Field(..., gt=0, description="Maximum number of attendees")
    start_time: datetime = Field(..., description="Event start time")
    created_at: datetime = Field(None, description="Event creation timestamp")
    updated_at: datetime = Field(None, description="Event last update timestamp")


class EventCreate(EventBase):
    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, v: datetime) -> datetime:
        """Ensure start_time is in the future."""
        # Ensure datetime is timezone-aware in UTC
        if v.tzinfo is None:
            raise ValueError("start_time must be timezone-aware.")

        # Convert to UTC if not already
        v_utc = v.astimezone(timezone.utc)

        # Ensure it's in the future
        if v_utc <= datetime.now(timezone.utc):
            raise ValueError("Event start time must be in the future.")

        return v_utc


class EventResponse(EventBase): ...
