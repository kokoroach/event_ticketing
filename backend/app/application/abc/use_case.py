import inspect
from abc import ABC, ABCMeta

from app.domain.abc.service import Service


class UseCaseMeta(ABCMeta):
    """Validates that each UseCase subclass defines a correct __init__()."""

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        # Skip validation on the base abstract class
        if cls.__name__ == "UseCase":
            return

        init = cls.__init__
        sig = inspect.signature(init)
        params = list(sig.parameters.values())[1:]  # Remove 'self'

        if not params:
            raise TypeError(
                f"{cls.__name__} must define at least one service dependency."
            )

        for p in params:
            if not p.name.endswith("_service"):
                raise TypeError(
                    f"Parameter '{p.name}' in {cls.__name__}.__init__ must end with"
                    " '_service'."
                )

            if p.annotation is inspect._empty:
                raise TypeError(
                    f"Parameter '{p.name}' in {cls.__name__}.__init__ must be"
                    "type-annotated."
                )

            # Check annotation is subclass of Service
            anno = p.annotation
            if not (isinstance(anno, type) and issubclass(anno, Service)):
                raise TypeError(
                    f"Parameter '{p.name}' in {cls.__name__}.__init__ must "
                    f"be a subclass of Service, got {anno}."
                )


class UseCase(ABC, metaclass=UseCaseMeta):
    """Base UseCase: execute has flexible arguments."""

    async def execute(self, *args, **kwargs):
        raise NotImplementedError
