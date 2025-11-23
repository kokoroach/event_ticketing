from contextlib import asynccontextmanager

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.v1 import deps as api_deps
from app.infrastructure.db.base import Base
from app.main import api

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# ------------------------------------------
# Database Fixtures
# ------------------------------------------
@pytest.fixture(scope="session")
async def test_db_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def test_session_factory(test_db_engine):
    session_factory = async_sessionmaker(
        bind=test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    yield session_factory


@pytest.fixture(scope="session")
async def test_db_session(test_session_factory):
    async with test_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()


# ------------------------------------------
# API Dependency Fixtures
# ------------------------------------------
@pytest.fixture(scope="session")
async def test_get_uow(test_session_factory):
    async for uow in api_deps._get_uow(test_session_factory):
        yield uow


@pytest.fixture(scope="session")
async def test_get_repo(test_get_uow):
    return api_deps.get_repo(test_get_uow)


@pytest.fixture
async def test_client_with_deps():
    @asynccontextmanager
    async def _get_client(dependency_override):
        for dep, override in dependency_override:
            api.dependency_overrides[dep] = override

        transport = ASGITransport(app=api)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

        api.dependency_overrides.clear()

    return _get_client
