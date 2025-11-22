from typing import Any, AsyncGenerator

from app.application.events.use_cases import CreateEventUseCase
from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.events.services import EventService
from app.infrastructure.db.session import AsyncSessionLocal


async def get_uow() -> AsyncGenerator[SQLAlchemyUnitOfWork, Any]:
    async with SQLAlchemyUnitOfWork(AsyncSessionLocal) as uow:
        yield uow


def get_create_event_uc() -> CreateEventUseCase:
    return CreateEventUseCase(EventService())
