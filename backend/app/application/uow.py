from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyUnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repo_cache: dict[type, Any] = {}

    async def __aenter__(self):
        self.session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.session is None:
            raise RuntimeError("Session was not initialized.")

        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    def get_repo(self, repo_cls: Any) -> Any:
        return repo_cls(self.session)
