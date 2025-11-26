from datetime import datetime
from typing import Any

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def from_orm(orm_obj: DeclarativeBase, dc_type: Any) -> Any:
    """
    Convert SQLAlchemy ORM model -> dataclass instance.
    Extract only DB columns, ignore anything extra.
    """
    data = {}
    for col in inspect(orm_obj).mapper.column_attrs:
        key = col.key
        value = getattr(orm_obj, key)

        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=settings.DEFAULT_TIMEZONE)
            else:
                value = value.astimezone(settings.DEFAULT_TIMEZONE)
        data[key] = value
    return dc_type(**data)
