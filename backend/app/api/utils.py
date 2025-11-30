from collections.abc import Iterable
from typing import Annotated, get_args

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from pydantic.json_schema import SkipJsonSchema


def _get_model_fields(class_bases: Iterable[type]) -> dict[str, FieldInfo]:
    """
    Collect and merge `model_fields` dictionaries from a sequence of base classes.
    """
    merged_fields: dict[str, FieldInfo] = {}

    for base in class_bases:
        merged_fields.update(getattr(base, "model_fields", {}))
    return merged_fields


class IgnoreSchemaMixin(BaseModel):
    """
    A mixin for Pydantic models that allows subclasses to specify fields to be
    excluded from the generated JSON schema via `ignore_in_schema`.

    To use this, define a `ignore_in_schema` attribute of type `ClassVar`

    Usage:
        >>> class Parent(BaseModel):
        ...     a: int
        ...     b: str
        ...
        >>> class Child(Parent, IgnoreSchemaMixin):
        ...     ignore_in_schema: ClassVar[list[str]] = ["b"]
    """

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        ignore_fields: Iterable[str] | None = getattr(cls, "ignore_in_schema", None)
        if ignore_fields is None:
            return

        # Validate type
        if not isinstance(ignore_fields, Iterable) or isinstance(ignore_fields, str):
            raise TypeError(
                "`ignore_in_schema` must be a sequence of field names "
                f"(e.g., list[str]). Got: {type(ignore_fields).__name__}"
            )

        ignore_fields = list(ignore_fields)

        # Gather base model fields from all parents
        base_fields = _get_model_fields(cls.__bases__)
        if not base_fields:
            return

        # Ensure the subclass has its own annotation dict
        cls.__annotations__ = dict(getattr(cls, "__annotations__", {}))

        for name in ignore_fields:
            if name not in base_fields:
                raise AttributeError(
                    f"`{name}` not found in any base model of {cls.__name__}"
                )

            orig_ann = base_fields[name].annotation
            # Replace annotation in the subclass BEFORE model creation4
            cls.__annotations__[name] = Annotated[
                SkipJsonSchema[orig_ann | None], Field(exclude=True)
            ]
            setattr(cls, name, None)


class AllOptionalMixin(BaseModel):
    """
    Mixin for Pydantic models that makes all defined and inherited fields optional
    while preserving existing Field metadata, validators, constraints, etc.
    """

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Ensure the subclass has its own annotation dict
        cls.__annotations__ = dict(getattr(cls, "__annotations__", {}))

        # Collect all base model fields
        all_fields = _get_model_fields(cls.__bases__ + (cls,))

        for name, field in all_fields.items():
            ann = field.annotation

            # Skip if already optional
            if type(ann) is type(None) or type(None) in get_args(ann):
                continue

            # Set default to None without losing other metadata
            field.default = None
            field.default_factory = None

            # Make type optional
            cls.__annotations__[name] = Annotated[ann | None, field]

            # Set default value to None
            setattr(cls, name, None)
