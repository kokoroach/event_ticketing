from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.infrastructure.db.models.base import ModelBase

async_engine = create_async_engine(
    str(settings.DATABASE_URI),
    echo=settings.DATABASE_ECHO,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)


async def db_shutdown():
    await async_engine.dispose()
