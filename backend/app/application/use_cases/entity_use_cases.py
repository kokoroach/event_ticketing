from app.application.events.use_cases import (
    CreateEventUseCase,
    GetEventUseCase,
    ListEventsUseCase,
    UpdateEventUseCase,
)
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository

from .base import ServiceSpec
from .use_case_factory import UseCaseFactory

# Store all services here
SERVICE_REGISTRY = {
    "event_service": ServiceSpec(EventService, SqlAlchemyEventRepository),
}

_UseCaseFactory = UseCaseFactory.register_services(SERVICE_REGISTRY)


class EventUseCases:
    create_event = _UseCaseFactory(CreateEventUseCase)  # type: ignore[call-arg]
    get_event = _UseCaseFactory(GetEventUseCase)  # type: ignore[call-arg]
    list_events = _UseCaseFactory(ListEventsUseCase)  # type: ignore[call-arg]
    update_event = _UseCaseFactory(UpdateEventUseCase)  # type: ignore[call-arg]
