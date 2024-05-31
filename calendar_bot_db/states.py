from aiogram.fsm.state import StatesGroup, State


class FSMCreateEvent(StatesGroup):
    fill_event_name = State()
    fill_event_date = State()
    fill_event_time = State()
    fill_event_details = State()


class FSMCreateMeeting(StatesGroup):
    fill_meeting_name = State()
    fill_meeting_date = State()
    fill_meeting_time = State()
    fill_meeting_duration = State()
    fill_meeting_participants = State()
    fill_meeting_details = State()


class FSMEditEvent(StatesGroup):
    choose_event = State()
    choose_event_point = State()
    edit_event_name = State()
    edit_event_date = State()
    edit_event_time = State()
    edit_event_details = State()


class FSMMenuOptions(StatesGroup):
    read_event = State()
    delete_event = State()
    read_meeting = State()
    delete_meeting = State()


class FSMRegistryUser(StatesGroup):
    fill_username = State()
    fill_email = State()
    fill_password = State()
