from typing import Any, AsyncGenerator

from fastapi import Depends

from app.application.events.use_cases import CreateEventUseCase
from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.db.session import AsyncSessionLocal


async def _get_uow() -> AsyncGenerator[SQLAlchemyUnitOfWork, Any]:
    async with SQLAlchemyUnitOfWork(AsyncSessionLocal) as uow:
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
    service: EventService = Depends(get_event_service),
) -> CreateEventUseCase:
    return CreateEventUseCase(service)
