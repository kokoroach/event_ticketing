from typing import Any, AsyncGenerator, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.events.use_cases import (
    CreateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    UpdateEventUseCase,
)
from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.abc.repository import Repository
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.db.session import AsyncSessionLocal


async def get_uow(
    session_factory: Callable[[], AsyncSession] | None = None,
) -> AsyncGenerator[SQLAlchemyUnitOfWork, Any]:
    if session_factory is None:
        session_factory = AsyncSessionLocal

    async with SQLAlchemyUnitOfWork(session_factory) as uow:
        yield uow


def get_repo(repo_cls: type[Repository]):
    async def wrapper(uow: SQLAlchemyUnitOfWork = Depends(get_uow)):
        return uow.get_repo(repo_cls)

    return wrapper


get_event_repo = get_repo(SqlAlchemyEventRepository)


def get_event_service(
    repo: SqlAlchemyEventRepository = Depends(get_event_repo),
) -> EventService:
    return EventService(repo=repo)


def create_event_uc(
    event_service: EventService = Depends(get_event_service),
) -> CreateEventUseCase:
    return CreateEventUseCase(event_service)


def get_event_uc(
    event_service: EventService = Depends(get_event_service),
) -> GetEventUseCase:
    return GetEventUseCase(event_service)


def list_events_uc(
    event_service: EventService = Depends(get_event_service),
) -> ListEventsUseCase:
    return ListEventsUseCase(event_service)


def update_event_uc(
    event_service: EventService = Depends(get_event_service),
) -> UpdateEventUseCase:
    return UpdateEventUseCase(event_service)
