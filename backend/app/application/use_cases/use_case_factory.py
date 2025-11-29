import inspect
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.session import AsyncSessionLocal

from .common import ServiceSpec
from .uow import SQLAlchemyUnitOfWork

T = TypeVar("T")


class UseCaseFactory(Generic[T]):  # noqa
    """
    This factory injects the services defined by the __init__ method from known
    SERVICE_REGSITRY.

    The services are likewise wrapped in a Unit of Work (UoW) pattern
    to have a share DB session. This ensures that commit and rollback are at the
    UseCase-level and not on service-level.
    """

    _services: dict[str, ServiceSpec] = {}

    def __init__(
        self,
        uc_class: type[T],
        session_factory: sessionmaker | None = AsyncSessionLocal,
    ):
        self._uc_class = uc_class
        self._uc_services: dict[str, ServiceSpec] = {}

        self._uow: SQLAlchemyUnitOfWork | None = None
        self._session_factory: Callable[[], AsyncSession] | None = session_factory

    @classmethod
    def register_services(
        cls, registry_services: dict[str, ServiceSpec]
    ) -> type["UseCaseFactory"]:
        for service in registry_services.values():
            if not isinstance(service, ServiceSpec):
                raise TypeError("All services must be instances of `ServiceSpec`.")

        # Clone the class
        new_cls: type[UseCaseFactory] = type(
            cls.__name__, cls.__bases__, dict(cls.__dict__)
        )
        new_cls._services = registry_services
        return new_cls

    def __call__(self):
        self._setup_uc_services()
        return self

    async def __aenter__(self) -> T:
        # Setup UoW
        if self._session_factory is None:
            raise RuntimeError("Session factory is not provided.")

        self._uow = SQLAlchemyUnitOfWork(self._session_factory)
        await self._uow.__aenter__()
        uc_services = await self._get_resolved_uc_services()
        return self._uc_class(**uc_services)

    def _setup_uc_services(self) -> None:
        if not self._services:
            raise RuntimeError(
                "Service registry is not set. Use 'register_services' first."
            )
        for service in self._get_use_case_services():
            try:
                self._uc_services[service] = self._services[service]
            except KeyError as e:
                raise RuntimeError(
                    f"Class service not found in the registry for `{service}`."
                ) from e

    async def __aexit__(self, exc_type, exc, tb):
        await self._uow.__aexit__(exc_type, exc, tb)

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
