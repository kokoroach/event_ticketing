from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as _mc


class TimestampMixin:
    """Mixin for models that need created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = _mc(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = _mc(
        DateTime(timezone=True),
        server_default=func.now(),
        # Note: server_onupdate doesn't work in SQLAlchemy 2.0
        onupdate=func.utcnow(),
    )
