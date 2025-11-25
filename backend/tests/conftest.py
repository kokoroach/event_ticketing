import asyncio
from contextlib import asynccontextmanager

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.api.v1 import deps as api_deps
from app.infrastructure.db.base import Base
from app.main import api

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# ------------------------------------------
# Database Fixtures
# ------------------------------------------
@pytest.fixture(scope="module")
async def test_db_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="module")
async def test_session_factory(test_db_engine):
    session_factory = async_sessionmaker(
        bind=test_db_engine, class_=AsyncSession, expire_on_commit=False
    )
    yield session_factory


@pytest.fixture(scope="function")
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
@pytest.fixture(scope="function")
async def test_get_uow(test_session_factory):
    async for uow in api_deps.get_uow(test_session_factory):
        yield uow


@pytest.fixture(scope="function")
async def test_get_event_repo(test_get_uow):
    return await api_deps.get_event_repo(test_get_uow)


@pytest.fixture(scope="function")
def test_client_with_deps():
    @asynccontextmanager
    async def _get_client(dependency_override):
        for dep, override in dependency_override:
            api.dependency_overrides[dep] = override

        transport = ASGITransport(app=api)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

        api.dependency_overrides.clear()

    return _get_client
