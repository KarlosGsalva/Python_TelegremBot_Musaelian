import logging

from aiogram import Router, F
from aiogram_dialog import DialogManager
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_events as db
from calendar_bot_db.states import FSMEditEvent

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import split_callback_to_name_id, convert_str_to_time

logger = logging.getLogger(__name__)

router = Router(name="edit_event_router")


@router.message(Command(commands=["3"]), StateFilter(default_state))
async def choose_event_for_edit(message: Message, state: FSMContext):
    keyboard = await kb.make_events_as_buttons(message.from_user.id)
    await message.answer(text=WTEXT["request_event_for_edit"], reply_markup=keyboard)
    await state.set_state(FSMEditEvent.choose_event)


@router.callback_query(StateFilter(FSMEditEvent.choose_event))
async def choose_event_point_for_edit(callback: CallbackQuery, state: FSMContext):
    event_id: int = split_callback_to_name_id(callback.data)["id"]
    user_tg_id: int = callback.from_user.id
    await state.update_data(event_id=event_id, user_tg_id=user_tg_id)
    await callback.message.answer(
        text=WTEXT["request_event_point_for_edit"],
        reply_markup=kb.make_event_points_as_buttons(),
    )
    await callback.answer()
    await state.set_state(FSMEditEvent.choose_event_point)


@router.callback_query(
    F.data == "change_event_name", StateFilter(FSMEditEvent.choose_event_point)
)
async def change_event_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(text=WTEXT["request_new_event_name"])
    await state.set_state(FSMEditEvent.edit_event_name)


@router.message(StateFilter(FSMEditEvent.edit_event_name))
async def edit_event_name(message: Message, state: FSMContext):
    new_event_name = message.text
    user_data = await state.get_data()

    # Изменяем событие
    await db.change_event(
        user_data["user_tg_id"], user_data["event_id"], new_event_name=new_event_name
    )

    # Добавляем в статистику
    await db.update_statistics(edited_events=True)
    await message.answer(WTEXT["event_name_edited"])
    await state.clear()


@router.callback_query(
    F.data == "change_event_date", StateFilter(FSMEditEvent.choose_event_point)
)
async def get_new_event_date(
    callback: CallbackQuery, state: FSMContext, dialog_manager: DialogManager
):
    await callback.answer()  # Подтверждаем получение callback
    await dialog_manager.start(FSMEditEvent.edit_event_date)


@router.callback_query(
    F.data == "change_event_time", StateFilter(FSMEditEvent.choose_event_point)
)
async def get_new_event_time(callback: CallbackQuery, state: FSMContext):
    keyboard = kb.time_keyboard()
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(
        text=WTEXT["request_new_event_time"], reply_markup=keyboard
    )
    await state.set_state(FSMEditEvent.edit_event_time)


@router.callback_query(
    F.data.startswith("time"), StateFilter(FSMEditEvent.edit_event_time)
)
async def edit_event_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с time
    # сохраняем время в datetime.time
    new_event_time = convert_str_to_time(callback.data[5:])

    # Сохраняем данные из state
    user_data = await state.get_data()

    # Изменяем событие
    await db.change_event(
        user_data["user_tg_id"], user_data["event_id"], new_event_time=new_event_time
    )

    # Добавляем в статистику
    await db.update_statistics(edited_events=True)

    # Уведомляем об успешном изменении данных
    await callback.message.answer(text=f"Новое время события: {new_event_time}")
    await callback.message.answer(WTEXT["event_time_edited"])
    await state.clear()


# Хэндлер 3 пункта меню, изменить описание события
@router.callback_query(
    F.data == "change_event_details", StateFilter(FSMEditEvent.choose_event_point)
)
async def request_new_event_details(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с выбором опции
    await callback.message.answer(WTEXT["request_new_event_details"])
    await state.set_state(FSMEditEvent.edit_event_details)


# Хэндлер меняющий описание выбранного события
@router.message(StateFilter(FSMEditEvent.edit_event_details))
async def set_new_event_details(message: Message, state: FSMContext):
    # Сохраняем новое описание события
    new_event_details = message.text

    # Сохраняем данные из state
    user_data = await state.get_data()

    # Изменяем событие
    await db.change_event(
        user_data["user_tg_id"],
        user_data["event_id"],
        new_event_details=new_event_details,
    )

    # Добавляем в статистику
    await db.update_statistics(edited_events=True)

    # Уведомляем об успешном изменении данных
    await message.answer(text=f"Новое описание события: {new_event_details}")
    await message.answer(WTEXT["event_details_edited"])
    await state.clear()
