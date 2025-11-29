from datetime import UTC, datetime
from typing import Annotated, ClassVar

from pydantic import BaseModel, Field, field_validator

from app.api.utils import AllOptionalMixin, IgnoreSchemaMixin


class EventBase(IgnoreSchemaMixin):
    id: Annotated[int, Field(description="Event ID")]
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
    created_at: Annotated[datetime, Field(description="Event creation timestamp")]
    updated_at: Annotated[datetime, Field(description="Event last update timestamp")]


class EventValidators(BaseModel):
    """Mixin to provide shared validations for Event models."""

    @field_validator("start_time", check_fields=False)
    @classmethod
    def validate_start_time(cls, v: datetime | None) -> datetime | None:
        # skip validation if field not provided (PATCH)
        if v is None:
            return None

        if v.tzinfo is None:
            raise ValueError("start_time must be timezone-aware")
        # Convert to UTC if not already
        v_utc = v.astimezone(UTC)
        # Ensure it's in the future
        if v_utc <= datetime.now(UTC):
            raise ValueError("start_time must be in the future")
        return v_utc


class EventCreateRequest(EventBase, EventValidators):
    ignore_in_schema: ClassVar = ["id", "created_at", "updated_at"]


class EventResponse(EventBase): ...


class PaginatedEventResponse(BaseModel):
    items: list[EventResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class EventUpdateRequest(EventCreateRequest, AllOptionalMixin, EventValidators): ...
