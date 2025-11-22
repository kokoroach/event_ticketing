from app.application.uow import SQLAlchemyUnitOfWork
from app.domain.events.entities import Event
from app.domain.events.services import EventService


class CreateEventUseCase:
    def __init__(self, service: EventService) -> None:
        self.service = service

    async def execute(self, uow: SQLAlchemyUnitOfWork, data: Event) -> Event:
        return await self.service.create_event(uow, data)
