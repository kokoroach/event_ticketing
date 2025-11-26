from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.v1.deps import (
    create_event_uc,
    get_event_uc,
    list_events_uc,
    update_event_uc,
)
from app.api.v1.schemas.events_schema import (
    EventCreateRequest,
    EventResponse,
    EventUpdateRequest,
    PaginatedEventResponse,
)
from app.application.events.use_cases import (
    CreateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    UpdateEventUseCase,
)

router = APIRouter()


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
)
async def create_event(
    data: EventCreateRequest,
    use_case: Annotated[CreateEventUseCase, Depends(create_event_uc)],
):
    return await use_case.execute(data)


@router.get(
    "/",
    response_model=PaginatedEventResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a paginated list of events",
)
async def list_events(
    *,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    use_case: Annotated[ListEventsUseCase, Depends(list_events_uc)],
):
    return await use_case.execute(page=page, page_size=page_size)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an event",
)
async def get_event(
    event_id: int,
    use_case: Annotated[GetEventUseCase, Depends(get_event_uc)],
):
    return await use_case.execute(event_id)


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an event",
)
async def update_event(
    event_id: int,
    data: EventUpdateRequest,
    use_case: Annotated[UpdateEventUseCase, Depends(update_event_uc)],
):
    return await use_case.execute(event_id, data)
