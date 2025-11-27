from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceSpec:
    service_class: type
    repo_class: type
