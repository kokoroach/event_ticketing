from typing import Annotated, get_args

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema


class IgnoreSchemaMixin(BaseModel):
    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        # If the subclass defines `ignore_in_schema``:
        ignore_fields = getattr(cls, "ignore_in_schema", [])
        if not ignore_fields:
            return

        # Get parent model fields (the real ones)
        if not cls.__bases__:
            return

        base = cls.__bases__[0]
        base_fields = getattr(base, "model_fields", {})

        for name in ignore_fields:
            if name not in base_fields:
                raise AttributeError(f"{name} not found in base model {base.__name__}")
            orig_ann = base_fields[name].annotation
            # Replace annotation in the subclass BEFORE model creation
            cls.__annotations__[name] = Annotated[
                SkipJsonSchema[orig_ann | None], Field(exclude=True)
            ]
            setattr(cls, name, None)


class AllOptionalMixin(BaseModel):
    """
    Mixin to make all fields optional while preserving all metadata.
    """

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for base in cls.__bases__:
            base_fields = getattr(base, "model_fields", {})
            for name, field in base_fields.items():
                orig_ann = field.annotation

                # Skip if already optional
                if type(orig_ann) is type(None) or type(None) in get_args(orig_ann):
                    continue

                # Make type optional
                cls.__annotations__[name] = Annotated[orig_ann | None, field]

                # Set default value to None
                setattr(cls, name, None)
