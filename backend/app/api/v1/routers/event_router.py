from fastapi import APIRouter, Depends

from app.api.v1.deps import get_create_event_uc, get_event_service
from app.api.v1.schemas.events_schema import EventCreate, EventResponse

router = APIRouter()


@router.post("/", response_model=EventResponse)
async def create_event(data: EventCreate, use_case=Depends(get_create_event_uc)):
    return await use_case.execute(data.model_dump())


@router.get("/", response_model=list[EventResponse])
async def list_events(service=Depends(get_event_service)):
    return await service.list_events()
