import logging

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_events as db
from calendar_bot_db.states import FSMMenuOptions

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import split_callback_to_name_id, convert_str_to_time

logger = logging.getLogger(__name__)

router = Router(name="delete_event_router")


# Хэндлер 4 пункта меню, удалить событие
@router.message(Command(commands=["4"]), StateFilter(default_state))
async def request_event_for_delete(message: Message, state: FSMContext):
    keyboard = await kb.make_events_as_buttons(message.from_user.id)
    await message.answer(text=WTEXT["request_event_for_delete"],
                         reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.delete_event)


# Хэндлер для удаления выбранного события
@router.callback_query(StateFilter(FSMMenuOptions.delete_event))
async def make_delete_event(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с выбором события
    event_name = split_callback_to_name_id(callback.data)["name"]
    event_id = split_callback_to_name_id(callback.data)["id"]
    await db.delete_event(callback.from_user.id, int(event_id))

    # Добавляем в статистику
    await db.update_statistics(canceled_events=True)
    await callback.message.answer(text=f"Событие {event_name} удалено.")
    await state.clear()
