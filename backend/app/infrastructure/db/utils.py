from typing import Any

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase


# TODO: Assert dc_type as actual dataclass in type hint
def from_orm(orm_obj: DeclarativeBase, dc_type: Any) -> Any:
    """
    Convert SQLAlchemy ORM model -> dataclass instance.
    Extract only DB columns, ignore anything extra.
    """
    data = {
        col.key: getattr(orm_obj, col.key)
        for col in inspect(orm_obj).mapper.column_attrs
        if col.key in dc_type.__dataclass_fields__
    }
    return dc_type(**data)
