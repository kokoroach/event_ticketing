from app.application.abc.use_case import UseCase
from app.application.events import use_cases as events_uc
from app.application.use_case_factory.common import ServiceSpec
from app.application.use_case_factory.use_case_factory import (
    UseCaseFactory,
    make_use_case_factory,
)
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.sqlalchemy.event_repo import (
    SqlAlchemyEventRepository,
)
from app.infrastructure.db.session import AsyncSessionLocal

# Store all services here
SERVICE_REGISTRY = {
    "event_service": ServiceSpec(EventService, SqlAlchemyEventRepository),
}
_UseCaseFactory = UseCaseFactory.register_services(SERVICE_REGISTRY)


def _make_use_case(use_case_cls: type[UseCase]) -> UseCaseFactory:
    """
    Creates a UseCase instance using the provided UseCase class,
    binding it to the appropriate factory and session.
    """
    if not issubclass(use_case_cls, UseCase):
        raise TypeError(f"{use_case_cls.__name__} must be a subclass of UseCase.")

    return make_use_case_factory(_UseCaseFactory, use_case_cls, AsyncSessionLocal)


class EventUseCases:
    create_event = _make_use_case(events_uc.CreateEventUseCase)
    get_event = _make_use_case(events_uc.GetEventUseCase)
    list_events = _make_use_case(events_uc.ListEventsUseCase)
    update_event = _make_use_case(events_uc.UpdateEventUseCase)
