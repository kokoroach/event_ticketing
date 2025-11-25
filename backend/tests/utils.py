import random
import string
from datetime import datetime

from sqlalchemy import inspect

characters = string.ascii_letters + string.digits


def is_timezone_aware(dt_obj: datetime) -> bool:
    tz_info = dt_obj.tzinfo
    return tz_info is not None and tz_info.utcoffset(dt_obj) is not None


def get_non_nullable_fields(
    model_class, except_for: list[str] | None = None
) -> list[str]:
    _except_for: set = set() if except_for is None else set(except_for)

    inspector = inspect(model_class)

    non_nullable_fields = []
    for column in inspector.mapper.columns:
        if not column.nullable and column.key not in _except_for:
            non_nullable_fields.append(column.key)
    return non_nullable_fields


def generate_random_string(k=7):
    return "".join(random.choices(characters, k=k))
