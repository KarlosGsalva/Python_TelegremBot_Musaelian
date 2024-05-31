import logging

from aiogram import Router, F
from aiogram_dialog import DialogManager, Dialog, setup_dialogs
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_events as db
from calendar_bot_db.states import FSMCreateEvent, FSMMenuOptions

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import split_callback_to_name_id

logger = logging.getLogger(__name__)

router = Router(name="show_event_detail_router")


@router.message(Command(commands=["2"]), StateFilter(default_state))
async def show_event(message: Message, state: FSMContext):
    # Выбираем событие инлайн кнопкой
    keyboard = await kb.make_events_as_buttons(message.from_user.id)
    await message.answer(text=WTEXT["request_event_for_show"],
                         reply_markup=keyboard)
    # Переводимся в состояние чтения заметки
    await state.set_state(FSMMenuOptions.read_event)


@router.callback_query(StateFilter(FSMMenuOptions.read_event))
async def show_requested_event(callback: CallbackQuery, state: FSMContext):
    event_id: int = split_callback_to_name_id(callback.data)["id"]
    user_tg_id: int = callback.from_user.id
    event_data = await db.read_selected_event(user_tg_id, event_id)
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(WTEXT["show_event"])
    await callback.message.answer(event_data)
    await state.clear()
