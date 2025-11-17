import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.base import Base

# 1️. Async database URL
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+asyncpg://admin:admin_pass@localhost:5432/ticketing_db"
)

# 2️. Create async engine
async_engine = create_async_engine(
    DATABASE_URI,
    echo=True,  # NOTE: Set to False in production
)

# 3️. Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# TODO: Create all Table
async def init_db() -> None:
    """Initialize Database"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# TODO adhoc
# loop = asyncio.get_event_loop()
# loop.create_task(init_db())


# 4️. Dependency to use in FastAPI
@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
