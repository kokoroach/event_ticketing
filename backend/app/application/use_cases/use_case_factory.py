import inspect
from typing import Any

from sqlalchemy.orm import sessionmaker

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

    _services: dict[str, ServiceSpec] = {}

    def __init__(
        self,
        uc_class: type[Any],
        session_factory: sessionmaker | None = AsyncSessionLocal,
    ):
        self._uc_class = uc_class
        self._uc_services: dict[str, ServiceSpec] = {}

        self._uow: SQLAlchemyUnitOfWork | None = None
        self._session_factory: sessionmaker | None = session_factory

    @classmethod
    def register_services(
        cls, registry_services: dict[str, ServiceSpec]
    ) -> type["UseCaseFactory"]:
        for service in registry_services.values():
            if not isinstance(service, ServiceSpec):
                raise TypeError("All services must be instances of `ServiceSpec`.")
        cls._services = registry_services
        return cls

    def __call__(self):
        self._setup_uc_services()
        return self

    async def __aenter__(self):
        # Setup UoW
        self._uow = SQLAlchemyUnitOfWork(self._session_factory)
        await self._uow.__aenter__()
        uc_services = await self._get_resolved_uc_services()
        return self._uc_class(**uc_services)

    def _setup_uc_services(self) -> None:
        if not self._services:
            raise RuntimeError(
                "Service registry is not set. Use 'register_services' first."
            )

        uc_services = self._get_use_case_services()
        self._uc_services = {
            name: spec for name, spec in self._services.items() if name in uc_services
        }

    async def __aexit__(self, exc_type, exc, tb):
        return await self._uow.__aexit__(exc_type, exc, tb)

    async def _get_resolved_uc_services(self) -> dict[str, Any]:
        assert self._uow

        uc_services = {}
        # Create service instances
        for name, spec in self._uc_services.items():
            repo = self._uow.get_repo(spec.repo_class)
            if not hasattr(repo, "session"):
                raise RuntimeError(
                    f"Repository for service {name} does not have a session attribute."
                )
            uc_services[name] = spec.service_class(repo)
        return uc_services

    def _get_use_case_services(self) -> set[str]:
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
        return set(req_services)
