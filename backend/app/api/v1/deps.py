from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.events.use_cases import CreateEventUseCase
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.db.session import get_session


async def get_event_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> SqlAlchemyEventRepository:
    return SqlAlchemyEventRepository(session)


def get_event_service(
    repo: Annotated[SqlAlchemyEventRepository, Depends(get_event_repository)]
) -> EventService:
    return EventService(repo)


def get_create_event_uc(
    service: Annotated[EventService, Depends(get_event_service)]
) -> CreateEventUseCase:
    return CreateEventUseCase(service)
