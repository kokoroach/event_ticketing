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


class EventUseCases:
    create_event = _UseCaseFactory(CreateEventUseCase)
    get_event = _UseCaseFactory(GetEventUseCase)
    list_events = _UseCaseFactory(ListEventsUseCase)
    update_event = _UseCaseFactory(UpdateEventUseCase)
