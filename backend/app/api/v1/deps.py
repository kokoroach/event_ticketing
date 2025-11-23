from typing import Any, AsyncGenerator, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.events.use_cases import CreateEventUseCase
from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.db.session import AsyncSessionLocal


async def _get_uow(
    session_factory: Callable[[], AsyncSession] | None = None,
) -> AsyncGenerator[SQLAlchemyUnitOfWork, Any]:
    if session_factory is None:
        session_factory = AsyncSessionLocal

    async with SQLAlchemyUnitOfWork(session_factory) as uow:
        yield uow


def get_repo(
    uow: SQLAlchemyUnitOfWork = Depends(_get_uow),
) -> SqlAlchemyEventRepository:
    return uow.get_repo(SqlAlchemyEventRepository)


def get_event_service(
    repo: SqlAlchemyEventRepository = Depends(get_repo),
) -> EventService:
    return EventService(repo=repo)


def get_create_event_uc(
    event_service: EventService = Depends(get_event_service),
) -> CreateEventUseCase:
    return CreateEventUseCase(event_service)
