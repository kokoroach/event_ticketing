from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as _mc

from app.infrastructure.db.base import Base

from .model_mixins import TimestampMixin


class EventModel(TimestampMixin, Base):
    __tablename__ = "events"

    id: Mapped[int] = _mc(Integer, primary_key=True, index=True)
    title: Mapped[str] = _mc(String(255), nullable=False)
    description: Mapped[str] = _mc(String(1000))
    event_type: Mapped[str] = _mc(String(255), nullable=False)
    venue: Mapped[str] = _mc(String(255), nullable=False)
    capacity: Mapped[int] = _mc(Integer, nullable=False)
    start_time: Mapped[datetime] = _mc(DateTime(timezone=True), nullable=False)
