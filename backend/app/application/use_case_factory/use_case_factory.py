import inspect
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.application.abc.use_case import UseCase
from app.application.uow.sqlalchemy_uow import SQLAlchemyUnitOfWork
from app.domain.abc.repository import Repository

from .common import ServiceSpec

T = TypeVar("T")


class UseCaseFactory(Generic[T]):  # noqa
    """
    A factory to instantiate Use Cases with their required services injected.

    Services are resolved from a registered SERVICE_REGISTRY and are wrapped
    in a Unit of Work (UoW) pattern to ensure all service repositories share the same
    database session. This guarantees that commit and rollback occur at the
    UseCase level rather than per-service.

    Usage:
        >>> MyFactory = UseCaseFactory.register_services(SERVICE_REGISTRY)
        >>>
        >>> # Create and use a use case instance inside an async context
        >>> async with MyFactory(MyUseCase, session_factory) as use_case:
        ...     await use_case.execute()
    """

    _registred_services: dict[str, ServiceSpec] = {}

    def __init__(
        self,
        uc_class: type[T],
        session_factory: sessionmaker,
    ):
        self._uc_class = uc_class
        self._uc_services: dict[str, ServiceSpec] = {}

        self._uow: SQLAlchemyUnitOfWork | None = None
        self._session_factory: Callable[[], AsyncSession] | None = session_factory

    @classmethod
    def register_services(
        cls, registry_services: dict[str, ServiceSpec]
    ) -> type["UseCaseFactory"]:
        """Register a dictionary of services for this factory class."""
        for service in registry_services.values():
            if not isinstance(service, ServiceSpec):
                raise TypeError("All services must be instances of `ServiceSpec`.")

        # Create a new subclass to avoid modifying the original
        new_cls: type[UseCaseFactory] = type(
            cls.__name__, cls.__bases__, dict(cls.__dict__)
        )
        new_cls._registred_services = registry_services
        return new_cls

    def __call__(self):
        """Prepare internal service mapping for the use case."""
        self._setup_uc_services()
        return self

    async def __aenter__(self) -> T:
        """Enter async context: initialize the Unit of Work and inject services."""
        if self._session_factory is None:
            raise RuntimeError("Session factory is not provided.")

        self._uow = SQLAlchemyUnitOfWork(self._session_factory)
        await self._uow.__aenter__()

        uc_services = await self._get_resolved_uc_services()
        return self._uc_class(**uc_services)

    def _setup_uc_services(self) -> None:
        """
        Inspect the UseCase constructor and map required services from the registry.
        """
        if not self._registred_services:
            raise RuntimeError(
                "Service registry is not set. Call 'register_services' first."
            )

        for service in self._get_use_case_services():
            try:
                self._uc_services[service] = self._registred_services[service]
            except KeyError as e:
                raise RuntimeError(
                    f"Class service not found in the registry for `{service}`."
                ) from e

    async def __aexit__(self, exc_type, exc, tb):
        await self._uow.__aexit__(exc_type, exc, tb)

    async def _get_resolved_uc_services(self) -> dict[str, Any]:
        """
        Instantiate service classes with their corresponding repository from the
        Unit of Work.
        """
        if self._uow is None:
            raise RuntimeError("Unit of Work is not initialized.")

        uc_services = {}

        for name, spec in self._uc_services.items():
            repo: Repository = self._uow.get_session_wrapped_repo(spec.repo_class)
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


def make_use_case_factory(
    uc_factory_cls: type[UseCaseFactory],
    use_case_cls: type[UseCase],
    session_factory: Callable[[], AsyncSession],
) -> UseCaseFactory:
    """
    Create a UseCaseFactory instance for the given use case class.

    This function helps instantiate a UseCaseFactory while preserving
    type information for type checkers and IDEs.
    """
    return uc_factory_cls(use_case_cls, session_factory)
