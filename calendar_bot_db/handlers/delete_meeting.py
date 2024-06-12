import logging

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_events as db
from calendar_bot_db.models import crud_meetings as dbm
from calendar_bot_db.states import FSMMenuOptions

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import split_callback_to_name_id

logger = logging.getLogger(__name__)

router = Router(name="delete_meeting_router")


# Хэндлер 9 пункта меню, удалить событие
@router.message(Command(commands=["9"]), StateFilter(default_state))
async def request_meeting_for_delete(message: Message, state: FSMContext):
    keyboard = await kb.make_meetings_as_buttons(message.from_user.id)
    await message.answer(
        text=WTEXT["request_meeting_for_delete"], reply_markup=keyboard
    )
    await state.set_state(FSMMenuOptions.delete_meeting)


# Хэндлер для удаления выбранного события
@router.callback_query(StateFilter(FSMMenuOptions.delete_meeting))
async def make_delete_event(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с выбором события
    meeting_name = split_callback_to_name_id(callback.data)["name"]
    meeting_id = split_callback_to_name_id(callback.data)["id"]
    await dbm.delete_meeting(callback.from_user.id, int(meeting_id))

    # Добавляем в статистику
    await db.update_statistics(canceled_meetings=True)
    await callback.message.answer(text=f"Событие {meeting_name} удалено.")
    await state.clear()
