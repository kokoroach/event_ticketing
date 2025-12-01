from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """Base Unit of Work Class"""

    @abstractmethod
    async def get_session_wrapped_repo(self, *args, **kwargs):
        raise NotImplementedError
