from unittest.mock import AsyncMock, MagicMock

import pytest

from app.application.use_cases.uow import SQLAlchemyUnitOfWork


class DummyRepo:
    def __init__(self, session):
        self.session = session


async def test_uow_aenter_initializes_session():
    mock_session = AsyncMock()
    session_factory = MagicMock(return_value=mock_session)
    uow = SQLAlchemyUnitOfWork(session_factory)

    async with uow as active_uow:
        assert active_uow.session is mock_session
        session_factory.assert_called_once()


async def test_uow_aexit_commits_on_success():
    mock_session = AsyncMock()
    uow = SQLAlchemyUnitOfWork(lambda: mock_session)

    async with uow:
        pass  # no exception

    mock_session.commit.assert_awaited_once()
    mock_session.rollback.assert_not_awaited()
    mock_session.close.assert_awaited_once()


async def test_uow_aexit_rolls_back_on_exception():
    mock_session = AsyncMock()
    uow = SQLAlchemyUnitOfWork(lambda: mock_session)

    class CustomError(Exception):
        pass

    with pytest.raises(CustomError):
        async with uow:
            raise CustomError("fail")

    mock_session.rollback.assert_awaited_once()
    mock_session.commit.assert_not_awaited()
    mock_session.close.assert_awaited_once()


async def test_get_repo_returns_repo_with_session():
    mock_session = AsyncMock()
    uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork(lambda: mock_session)

    async with uow:
        repo = uow.get_session_wrapped_repo(DummyRepo)

        # Assertions
        assert isinstance(repo, DummyRepo)
        assert repo.session is mock_session
