import asyncio
from contextlib import asynccontextmanager

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.infrastructure.db.base import Base
from app.main import api

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def test_event_loop():
    """Create an event loop for the entire test session."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def test_db_session(test_engine):
    async_session = async_sessionmaker(test_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
def test_usecase_builder():
    def _build(usecase_cls, *services):
        if len(services) == 1:
            return usecase_cls(services[0])
        return usecase_cls(*services)

    return _build


@pytest.fixture
async def test_client_with_dep():
    @asynccontextmanager
    async def _get_client(dependency, dependency_override):
        async def _override():
            yield dependency_override

        api.dependency_overrides[dependency] = _override

        transport = ASGITransport(app=api)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client

        api.dependency_overrides.clear()

    return _get_client
