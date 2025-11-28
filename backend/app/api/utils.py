from typing import Optional, get_type_hints

from pydantic import BaseModel, create_model


def make_optional_model(base_model: BaseModel, model_name: str) -> BaseModel:
    """
    Create a new Pydantic model where all non-optional fields from `base_model`
    are converted to optional fields (for PATCH use).
    """
    annotations = get_type_hints(base_model)
    new_fields: dict[str, tuple] = {}

    for field_name, field_type in annotations.items():
        # Skip already optional fields
        if getattr(field_type, "__origin__", None) is Optional:
            new_fields[field_name] = (field_type, getattr(base_model, field_name, None))
        else:
            # Make field optional and set default None
            new_fields[field_name] = (field_type | None, None)

    return create_model(model_name, **new_fields)
