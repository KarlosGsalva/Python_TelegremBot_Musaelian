import logging

from aiogram import Router, F
from aiogram_dialog import DialogManager, Dialog, setup_dialogs
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_sqla_core as db
from calendar_bot_db.states import FSMCreateEvent

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import convert_str_to_time

logger = logging.getLogger(__name__)

router = Router(name="create_event_router")


# Обрабатываем команду /1: Создать событие
@router.message(Command(commands=["1"]), StateFilter(default_state))
async def create_event(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WTEXT["request_event_name"],
                         reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateEvent.fill_event_name)


# Забираем название события, переключаемся на введение даты
@router.message(StateFilter(FSMCreateEvent.fill_event_name))
async def process_event_name(message: Message, state: FSMContext,
                             dialog_manager: DialogManager):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(event_name=message.text)
    # отправляем календарь
    await dialog_manager.start(FSMCreateEvent.fill_event_date)


# Забираем дату события, переключаемся на введение details
@router.callback_query(F.data.startswith("time"), StateFilter(FSMCreateEvent.fill_event_time))
async def process_event_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с time
    event_time = callback.data[5:]
    await callback.message.answer(f"Вы выбрали {event_time} временем события.")
    await state.update_data(event_time=event_time)
    await callback.message.answer(WTEXT["request_event_details"])
    await state.set_state(FSMCreateEvent.fill_event_details)


# Забираем описание и записываем событие в БД
@router.message(StateFilter(FSMCreateEvent.fill_event_details))
async def write_event_details(message: Message, state: FSMContext):
    await state.update_data(details=message.text)

    # Собираем данные из state
    event_data = await state.get_data()
    user_tg_id = event_data["user_tg_id"]
    event_name = event_data["event_name"]
    event_date = event_data["event_date"]
    event_time = convert_str_to_time(event_data["event_time"])
    event_details = event_data["details"]

    # Записываем в БД
    await db.write_event_in_db(user_tg_id, event_name, event_date, event_time, event_details)
    await db.update_statistics(event_count=True)
    await message.answer(WTEXT["event_made"])
    await state.clear()
