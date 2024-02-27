from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

storage = MemoryStorage()


class FSMFillEvent(StatesGroup):
    fill_event_name = State()
    fill_event_date = State()
    fill_event_time = State()
    fill_event_details = State()


class FSMMenuOptions(StatesGroup):
    read_event = State()
    edit_event = State()
    choose_event = State()
    choose_event_point = State()
    delete_event = State()