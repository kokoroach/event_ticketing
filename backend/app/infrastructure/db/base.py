# app/infrastructure/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared Base class for all SQLAlchemy ORM models."""

    pass
