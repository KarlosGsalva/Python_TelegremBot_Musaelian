import pytest

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from calendar_bot_db.handlers import get_routers
from calendar_bot_db.tests.mocked_aiogram import MockedBot, MockedSession


@pytest.fixture(scope="session")
def dp() -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_routers(*get_routers(dispatcher))
    return dispatcher


@pytest.fixture(scope="function")
def bot() -> MockedBot:
    bot = MockedBot()
    bot.session = MockedSession()
    return bot


@pytest.fixture(scope="function", autouse=True)
def clear_queues(bot: MockedBot):
    yield
    bot.session.responses.clear()
    bot.session.requests.clear()
