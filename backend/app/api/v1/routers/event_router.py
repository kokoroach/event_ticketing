from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.v1.deps import get_create_event_uc, get_uow
from app.api.v1.schemas.events_schema import EventCreate, EventResponse
from app.application.events.use_cases import CreateEventUseCase
from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.events.entities import Event

router = APIRouter()


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new event",
)
async def create_event(
    data: EventCreate,
    use_case: Annotated[CreateEventUseCase, Depends(get_create_event_uc)],
    uow: Annotated[SQLAlchemyUnitOfWork, Depends(get_uow)],
):
    event_data = Event(**data.model_dump())
    return await use_case.execute(uow, event_data)


# @router.get("/", response_model=list[EventResponse])
# async def list_events(service: Annotated[EventService, Depends(get_event_service)]):
#     return await service.list_events()
