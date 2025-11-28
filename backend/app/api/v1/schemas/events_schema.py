from datetime import UTC, datetime
from typing import Annotated, cast

from pydantic import BaseModel, Field, field_validator

from app.api.utils import make_optional_model


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


class EventCreateRequest(EventBase, EventValidators): ...


class EventResponse(EventBase): ...


class PaginatedEventResponse(BaseModel):
    items: list[EventResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


EventUpdateRequestBase: type[BaseModel] = cast(
    type[BaseModel], make_optional_model(EventBase, "EventUpdateRequest")
)


class EventUpdateRequest(EventUpdateRequestBase, EventValidators): ...
