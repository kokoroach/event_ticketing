from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column as _mc

from .base import ModelBase


class EventModel(ModelBase):
    __tablename__ = "events"

    title: Mapped[str] = _mc(String(255), nullable=False)
    description: Mapped[str] = _mc(String(1000))
    event_type: Mapped[str] = _mc(String(255), nullable=False)
    venue: Mapped[str] = _mc(String(255), nullable=False)
    capacity: Mapped[int] = _mc(Integer, nullable=False)
    start_time: Mapped[datetime] = _mc(DateTime(timezone=True), nullable=False)
