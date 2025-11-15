from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.db.session import get_session
from fastapi import Depends


async def get_event_repository():
    async with get_session() as session:
        yield SqlAlchemyEventRepository(session)


async def get_event_service(repo=Depends(get_event_repository)):
    return EventService(repo)


async def get_create_event_uc(service=Depends(get_event_service)):
    return CreateEventUseCase(service)
