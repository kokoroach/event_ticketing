from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository
from app.infrastructure.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.events.use_cases import (
    CreateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    UpdateEventUseCase,
)

from dataclasses import dataclass
from typing import Type, Any
import inspect


@dataclass(frozen=True)
class ServiceSpec:
    service_class: type
    repo_class: type


# Store all services here
SERVICE_REGISTRY = {
    "event_service": ServiceSpec(EventService, SqlAlchemyEventRepository),
}


class UseCaseFactory:
    """
    This factory wraps the services to be used by every use case to use the Unit
    of Work (UoW) for their DB sessions.

    This ensures that commit and rollback are at the UseCase-level and not on
    service-level.
    """

    def __init__(self, uc_class: Type[Any]):
        self.uc_class = uc_class
        self.services: dict[str, ServiceSpec] = {}
        self.uow: SQLAlchemyUnitOfWork | None = None
        self.service_instances: dict[str, type] = {}
        self._service_sessions: list[AsyncSession] = []

        self._setup_services()

    def _setup_services(self) -> None:
        req_services = self._get_use_case_services()
        self.services = {name: SERVICE_REGISTRY[name] for name in req_services}

    def _get_use_case_services(self) -> list[str]:
        """Inspect the use case constructor to determine required services."""
        params = inspect.signature(self.uc_class.__init__).parameters
        req_services = [
            name
            for name, param in params.items()
            if name != "self"
            and param.default is param.empty
            and name.endswith("_service")
        ]
        if not req_services:
            raise RuntimeError(f"No services were indicated for {self.uc_class}")
        return req_services

    def __call__(self):
        return self

    async def _build_services(self):
        # Create service instances and track their sessions
        for name, spec in self.services.items():
            repo = self.uow.get_repo(spec.repo_class)

            if hasattr(repo, "session"):
                self._service_sessions.append(repo.session)
            else:
                raise RuntimeError(
                    f"Repository for service {name} does not have a session attribute"
                )

            service = spec.service_class(repo)
            self.service_instances[name] = service

    async def _close_service_sessions(self):
        for session in self._service_sessions:
            await session.close()

    async def __aenter__(self):
        # Setup UoW
        self.uow = SQLAlchemyUnitOfWork(AsyncSessionLocal)
        await self.uow.__aenter__()
        await self._build_services()

        return self.uc_class(**self.service_instances)

    async def __aexit__(self, exc_type, exc, tb):
        # Close service sessions first
        await self._close_service_sessions()
        # Then exit UoW
        return await self.uow.__aexit__(exc_type, exc, tb)


class EventUseCases:
    create_event = UseCaseFactory(CreateEventUseCase)
    get_event = UseCaseFactory(GetEventUseCase)
    list_events = UseCaseFactory(ListEventsUseCase)
    update_event = UseCaseFactory(UpdateEventUseCase)
