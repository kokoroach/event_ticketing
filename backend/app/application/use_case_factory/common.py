from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceSpec:
    """
    Specification for a service and its associated repository.
    """

    service_class: type
    repo_class: type
