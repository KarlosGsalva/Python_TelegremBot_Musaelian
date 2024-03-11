from aiogram import Dispatcher
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class FSMCreateEvent(StatesGroup):
    fill_event_name = State()
    fill_event_date = State()
    fill_event_time = State()
    fill_event_details = State()


class FSMEditEvent(StatesGroup):
    choose_event = State()
    choose_event_point = State()
    edit_event_date = State()
    edit_event_time = State()
    edit_event_details = State()


class FSMMenuOptions(StatesGroup):
    read_event = State()
    delete_event = State()
