from app.domain.abc.repository import Repository

from .entities import Event


class EventRepository(Repository[Event]): ...
