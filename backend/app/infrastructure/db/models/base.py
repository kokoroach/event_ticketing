from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column as _mc

from app.core.config import settings


class Base(DeclarativeBase):
    """Shared Base class for all SQLAlchemy ORM models."""

    id: Mapped[int] = _mc(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = _mc(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = _mc(
        DateTime(timezone=True),
        server_default=func.now(),
        # Note: server_onupdate doesn't work in SQLAlchemy 2.0
        onupdate=lambda: datetime.now(settings.DEFAULT_TIMEZONE),
    )
