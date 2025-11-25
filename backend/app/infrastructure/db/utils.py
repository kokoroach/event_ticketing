from datetime import UTC, datetime
from typing import Any

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


# TODO: Generalize app's datetime TZ in config's setting
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
                value = value.replace(tzinfo=UTC)
            else:
                value = value.astimezone(UTC)
        data[key] = value
    return dc_type(**data)
