from typing import Any, AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.events.use_cases import CreateEventUseCase
from app.application.uow import UnitOfWork
from app.domain.events.services import EventService
from app.infrastructure.db.session import AsyncSessionLocal


async def get_uow(
    session_factory: Callable[[], AsyncSession] = AsyncSessionLocal,
) -> AsyncGenerator[UnitOfWork, Any]:
    async with UnitOfWork(session_factory) as uow:
        yield uow


def get_create_event_uc() -> CreateEventUseCase:
    return CreateEventUseCase(EventService())
