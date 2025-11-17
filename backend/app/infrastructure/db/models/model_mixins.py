from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as _mc


class TimestampMixin:
    created_at: Mapped[datetime] = _mc(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = _mc(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
