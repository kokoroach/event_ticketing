from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class EventBase(BaseModel):
    id: Annotated[int | None, Field(description="Event ID")] = None
    title: Annotated[str, Field(min_length=1, max_length=255)]
    description: Annotated[
        str, Field(min_length=1, max_length=1000, description="Event description")
    ]
    event_type: Annotated[
        str, Field(min_length=1, max_length=255, description="Type of event")
    ]
    venue: Annotated[
        str, Field(min_length=1, max_length=255, description="Event venue")
    ]
    capacity: Annotated[int, Field(gt=0, description="Maximum number of attendees")]
    start_time: Annotated[datetime, Field(description="Event start time")]
    created_at: Annotated[
        datetime | None, Field(description="Event creation timestamp")
    ] = None
    updated_at: Annotated[
        datetime | None, Field(description="Event last update timestamp")
    ] = None


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
