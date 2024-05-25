import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from calendar_bot_db.states import FSMCreateMeeting
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb


logger = logging.getLogger(__name__)

router = Router(name="create_meeting_router")


# Хэндлер для создания встречи
@router.message(Command(commands=["7"]), StateFilter(default_state))
async def create_meeting(message: Message, state: FSMContext):
    await message.answer(WTEXT["request_meeting_name"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_name)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_name))
async def get_meeting_name(message: Message, state: FSMContext, dialog: DialogManager):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(meeting_name=message.text)
    await dialog.start(FSMCreateMeeting.fill_meeting_date)


@router.callback_query(F.data.startswith("time"), StateFilter(FSMCreateMeeting.fill_meeting_time))
async def set_event_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    meeting_time = callback.data[5:]
    await callback.message.answer(f"Вы выбрали {meeting_time} временем встречи.")



