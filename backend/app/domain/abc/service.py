import inspect
from abc import ABCMeta

from .repository import Repository


class ServiceMeta(ABCMeta):
    """Ensures each Service subclass receives at least one Repository."""

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

        # Skip the base Service class itself
        if cls.__name__ == "Service":
            return

        init = cls.__init__
        sig = inspect.signature(init)
        params = list(sig.parameters.values())[1:]  # skip "self"

        if not params:
            raise TypeError(
                f"{cls.__name__} must define at least one repository dependency."
            )

        repo_found = False

        for p in params:
            # Variable args like *args or **kwargs are not allowed for
            # DI-enforced classes
            if p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
                raise TypeError(
                    f"{cls.__name__}.__init__ cannot use *args or **kwargs."
                )

            if p.annotation is inspect._empty:
                raise TypeError(
                    f"Parameter '{p.name}' in {cls.__name__}.__init__ must be"
                    " type-annotated."
                )

            anno = p.annotation
            if isinstance(anno, type) and issubclass(anno, Repository):
                repo_found = True

        if not repo_found:
            raise TypeError(
                f"{cls.__name__} must have at least one dependency annotated "
                f"with a subclass of Repository."
            )


class Service(metaclass=ServiceMeta):
    """Base class for all services."""

    ...
