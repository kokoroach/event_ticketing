from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork:
    def __init__(self, session_factory: Any) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._repo_cache: dict[type, Any] = {}

    async def __aenter__(self):
        self.session = self._session_factory()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self.session

        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    def get_repo(self, repo_cls: Any) -> Any:
        if repo_cls not in self._repo_cache:
            self._repo_cache[repo_cls] = repo_cls(self.session)
        return self._repo_cache[repo_cls]
