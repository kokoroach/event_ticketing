import inspect
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import AsyncSessionLocal

from .common import ServiceSpec
from .uow import SQLAlchemyUnitOfWork


class UseCaseFactory:
    """
    This factory wraps the services to be used by every use case to use the Unit
    of Work (UoW) for their DB sessions.

    This ensures that commit and rollback are at the UseCase-level and not on
    service-level.
    """

    def __init__(self, uc_class: type[Any]):
        self._uc_class = uc_class
        self._services: dict[str, ServiceSpec] = {}
        self._uc_services: dict[str, ServiceSpec] = {}

        self._uow: SQLAlchemyUnitOfWork | None = None
        self._service_instances: dict[str, type] = {}
        self._service_sessions: dict[str, AsyncSession] = {}

    @classmethod
    def register_services(
        cls, registry_services: dict[str, ServiceSpec]
    ) -> type["UseCaseFactory"]:
        for service in registry_services.values():
            if not isinstance(service, ServiceSpec):
                raise TypeError("All services must be instances of `ServiceSpec`.")
        cls._services = registry_services
        return cls

    def _setup_uc_services(self) -> None:
        if not self._services:
            raise RuntimeError(
                "Service registry is not set. Use 'register_services' first."
            )

        req_services = self._get_use_case_services()
        self._uc_services = {name: self._services[name] for name in req_services}

    def __call__(self):
        self._setup_uc_services()

    async def __aenter__(self):
        # Setup UoW
        self.uow = SQLAlchemyUnitOfWork(AsyncSessionLocal)
        await self.uow.__aenter__()
        await self._build_services()

        return self._uc_class(**self._service_instances)

    async def __aexit__(self, exc_type, exc, tb):
        # Close service sessions first
        await self._close_service_sessions()
        # Then exit UoW
        return await self.uow.__aexit__(exc_type, exc, tb)

    async def _build_services(self):
        # Create service instances and track their sessions
        for name, spec in self._uc_services.items():
            repo = self._uow.get_repo(spec.repo_class)

            if not hasattr(repo, "session"):
                raise RuntimeError(
                    f"Repository for service {name} does not have a session attribute."
                )

            self._service_instances[name] = spec.service_class(repo)
            self._service_sessions[name] = repo.session

    def _get_use_case_services(self) -> list[str]:
        """Inspect the use case constructor to determine required services."""
        params = inspect.signature(self._uc_class.__init__).parameters
        req_services = [
            name
            for name, param in params.items()
            if name != "self"
            and param.default is param.empty
            and name.endswith("_service")
        ]
        if not req_services:
            raise RuntimeError(f"No services were indicated for {self._uc_class}")
        return req_services

    async def _close_service_sessions(self):
        for session in self._service_sessions.values():
            await session.close()
