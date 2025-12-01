from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.abc.repository import Repository


class SQLAlchemyUnitOfWork:
    """
    Async Unit of Work (UoW) pattern for SQLAlchemy.

    Usage:
    >>> async with SQLAlchemyUnitOfWork(session_factory) as uow:
    >>>     repo = uow.get_session_wrapped_repo(SomeRepo)
    >>>     await repo.do_something()
    """

    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self.session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.session is None:
            raise RuntimeError("Session was not initialized.")

        try:
            if exc:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()

    def get_session_wrapped_repo(self, repo_class: type[Repository]) -> Repository:
        """
        Return a repository instance bound to the current session.
        Caches instances to ensure one repo per class per UnitOfWork.
        """
        return repo_class(self.session)
