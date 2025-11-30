from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.api.v1.schemas.events_schema import EventCreateRequest
from app.application.use_cases.common import ServiceSpec
from app.application.use_cases.entity_use_cases import SERVICE_REGISTRY
from app.application.use_cases.use_case_factory import UseCaseFactory
from app.domain.events.entities import Event
from app.domain.events.services import EventService
from app.infrastructure.db.repositories.event_repo import SqlAlchemyEventRepository


class BareUseCase:
    def __init__(self):
        pass

    def execute(self):
        pass


class SampleUseCase:
    def __init__(self, unknown_service: Any):
        pass

    def execute(self):
        pass


class CustomCreateEventUseCase:
    def __init__(self, event_service: EventService, sample_service: EventService):
        self._event_service = event_service
        self._sample_service = sample_service

    async def execute_happy_case(self, data: EventCreateRequest) -> Event:
        """
        Create 3 events using the services.

        Note: `sample_service` is essentially a clone of event service
        """
        await self._event_service.create_event(data)
        await self._sample_service.create_event(data)
        return await self._event_service.create_event(data)

    async def execute_not_happy_case(self, data: EventCreateRequest) -> Event:
        """
        Attempt to create 3 events using the services but got some arbitrary exception
        """
        await self._event_service.create_event(data)
        await self._sample_service.create_event(data)
        await self._event_service.create_event(data)
        raise RuntimeError("Simulated RunTimeError")


# Update service registry for testing
sample_service = {
    "sample_service": ServiceSpec(EventService, SqlAlchemyEventRepository),
}
SERVICE_REGISTRY.update(sample_service)

UseCaseFactoryWithServices = UseCaseFactory.register_services(SERVICE_REGISTRY)


event_data = {
    "title": "Concert",
    "description": "Some descr here.",
    "event_type": "concert",
    "venue": "Manila City",
    "start_time": datetime.now(UTC) + timedelta(weeks=6),
    "capacity": 5,
}


class TestUseCaseFactoryGroup:
    async def test_use_case_factory_not_called(self, test_session_factory):
        """
        Test that the factory's __call__ is awaited.

        Calling a factory generated `bare_uc` instead of `bare_uc()`
        """
        bare_uc = UseCaseFactory(BareUseCase, test_session_factory)

        with (
            pytest.raises(AssertionError),
            patch.object(bare_uc, "__call__", new_callable=AsyncMock) as mock_call,
        ):
            async with bare_uc as use_case:
                use_case.execute()

            mock_call.assert_awaited_once()

    async def test_use_case_factory_having_no_registred_services(
        self, test_session_factory
    ):
        """Raises RuntimeError if service registry is not set."""

        bare_uc = UseCaseFactory(BareUseCase, test_session_factory)

        with pytest.raises(RuntimeError, match=r"^Service registry is not set"):
            async with bare_uc() as use_case:
                use_case.execute()

    async def test_use_case_factory_with_no_service(self):
        """
        Raises RuntimeError if a required service is missing in the registry

        Use case classes need to have at least one service as parameter, in the form:
        "<entity>_service".

        >>> class SomeUseCase:
        >>>     def __init__(self, <entity>_service):
        >>>         ...
        """
        mock_session = AsyncMock()
        session_factory = MagicMock(return_value=mock_session)

        sample_uc = UseCaseFactoryWithServices(SampleUseCase, session_factory)
        with pytest.raises(
            RuntimeError, match=r"^Class service not found in the registry for"
        ):
            async with sample_uc() as use_case:
                use_case.execute()

    async def test_use_case_factory_services_share_session(self, test_session_factory):
        """EventService and SampleService share the same session."""
        test_event_uc = UseCaseFactoryWithServices(
            CustomCreateEventUseCase, test_session_factory
        )
        async with test_event_uc() as use_case:
            event_session_id = id(use_case._event_service._repo.session)
            sample_session_id = id(use_case._sample_service._repo.session)

            assert event_session_id == sample_session_id

    async def test_use_case_factory_not_happy_case(self, test_session_factory):
        """Test that all service ORM changes are rolled back on exception."""
        # pass test DB session
        test_event_uc: UseCaseFactory[CustomCreateEventUseCase] = (
            UseCaseFactoryWithServices(CustomCreateEventUseCase, test_session_factory)
        )
        try:
            async with test_event_uc() as use_case:
                req_event_data = EventCreateRequest(**event_data)
                await use_case.execute_not_happy_case(req_event_data)
        except Exception:
            ...

        # This is hacky check
        async with test_event_uc() as use_case:
            events, total = await use_case._event_service.list_events(
                offset=0, limit=10
            )
            assert (events, total) == ([], 0)

    async def test_use_case_factory_happy_case(self, test_session_factory):
        """Test that all service ORM changes are committed as one transaction."""
        test_event_uc: UseCaseFactory[CustomCreateEventUseCase] = (
            UseCaseFactoryWithServices(CustomCreateEventUseCase, test_session_factory)
        )

        async with test_event_uc() as use_case:
            req_event_data = EventCreateRequest(**event_data)
            result = await use_case.execute_happy_case(req_event_data)

            # Created 3 instances
            assert result.id == 3
