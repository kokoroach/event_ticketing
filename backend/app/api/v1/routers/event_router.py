from typing import Annotated

from fastapi import APIRouter, Query, status

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
from app.application.use_cases import EventUseCaseFactory

router = APIRouter()


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
)
async def create_event(
    data: EventCreateRequest,
):
    use_case = await EventUseCaseFactory(CreateEventUseCase)
    return await use_case.execute(data)


@router.get(
    "/",
    response_model=PaginatedEventResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a paginated list of events",
)
async def list_events(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    use_case = await EventUseCaseFactory(ListEventsUseCase)
    return await use_case.execute(page=page, page_size=page_size)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    summary="Get an event",
)
async def get_event(
    event_id: int,
):
    use_case = await EventUseCaseFactory(GetEventUseCase)
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
):
    use_case = await EventUseCaseFactory(UpdateEventUseCase)
    return await use_case.execute(event_id, data)
