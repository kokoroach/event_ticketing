import asyncio
from types import SimpleNamespace

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.application.use_cases.entity_use_cases import _UseCaseFactory
from app.infrastructure.db.models.base import Base

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
# Usecase Fixture
# # ------------------------------------------
@pytest.fixture(scope="module")
def test_use_case(test_session_factory):
    """
    Fixture that dynamically initializes use cases with the test session factory.
    Returns a namespace object with the use cases as attributes.

    The aim is to create a test version of use cases in
    `app.application.use_cases.entity_use_cases`
    """

    def wrapper(use_cases: dict[str, type]):
        uc = SimpleNamespace()
        for attr_name, uc_class in use_cases.items():
            setattr(uc, attr_name, _UseCaseFactory(uc_class, test_session_factory))
        return uc

    return wrapper
