from typing import TypeVar

from app.application.events.use_cases import (
    CreateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    UpdateEventUseCase,
)
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository

from .common import ServiceSpec
from .use_case_factory import UseCaseFactory

# Store all services here
SERVICE_REGISTRY = {
    "event_service": ServiceSpec(EventService, SqlAlchemyEventRepository),
}

_UseCaseFactory = UseCaseFactory.register_services(SERVICE_REGISTRY)


T = TypeVar("T")


def make_factory(use_case_cls: type[T]) -> UseCaseFactory[T]:  # noqa
    """
    Create a UseCaseFactory instance for the given use case class.

    This function helps instantiate a UseCaseFactory while preserving
    type information for type checkers and IDEs.
    """
    return _UseCaseFactory(use_case_cls)


class EventUseCases:
    create_event = make_factory(CreateEventUseCase)
    get_event = make_factory(GetEventUseCase)
    list_events = make_factory(ListEventsUseCase)
    update_event = make_factory(UpdateEventUseCase)
