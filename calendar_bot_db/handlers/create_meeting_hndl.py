import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from calendar_bot_db.models import crud_events as db
from calendar_bot_db.models import crud_meetings as dbm
from calendar_bot_db.models.config import async_engine
from calendar_bot_db.services import convert_str_to_time
from calendar_bot_db.states import FSMCreateMeeting
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb

from datetime import datetime as dt, timedelta

logger = logging.getLogger(__name__)

router = Router(name="create_meeting_router")


# Хэндлер для создания встречи
@router.message(Command(commands=["7"]), StateFilter(default_state))
async def create_meeting(message: Message, state: FSMContext):
    await message.answer(WTEXT["request_meeting_name"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_name)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_name))
async def get_meeting_name(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(meeting_name=message.text)
    await dialog_manager.start(FSMCreateMeeting.fill_meeting_date)


@router.callback_query(F.data.startswith("time"), StateFilter(FSMCreateMeeting.fill_meeting_time))
async def set_meeting_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    meeting_time = callback.data[5:]
    await callback.message.answer(f"Вы выбрали {meeting_time} временем встречи.")
    await state.update_data(meeting_time=meeting_time)
    await callback.message.answer(WTEXT["request_meeting_duration"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_duration)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_duration))
async def set_meeting_duration(message: Message, state: FSMContext):
    duration = message.text

    if duration.isdigit():
        await message.answer(f"Планируемое время встречи {duration} минут.")
        await state.update_data(duration=duration, participants=[])
        keyboard = await kb.make_users_as_buttons(message.from_user.id)
        await message.answer(WTEXT["request_meeting_participants"], reply_markup=keyboard)
        await state.set_state(FSMCreateMeeting.fill_meeting_participants)
    else:
        await message.answer(WTEXT["duration_warning"])
        await message.answer(WTEXT["request_meeting_details"], reply_markup=kb.cancel_markup)


@router.callback_query(F.data != "participants_selected",
                       StateFilter(FSMCreateMeeting.fill_meeting_participants))
async def get_participants(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    participants = data["participants"]
    user_id = callback.data

    # Проверка занятости времени участников
    async with async_engine.begin() as connection:
        meeting_date_str = data.get("meeting_date")
        meeting_date = dt.strptime(meeting_date_str, "%d.%m.%Y").date()
        meeting_time = dt.strptime(data.get("meeting_time"), "%H:%M").time()
        meeting_duration = timedelta(minutes=int(data.get("duration")))

        is_busy = await dbm.is_user_available(connection, user_id, meeting_date,
                                              meeting_time, meeting_duration)

    if is_busy:
        await callback.answer("У выбранного пользователя уже назначена встреча на это время",
                              show_alert=True)
    else:
        if user_id in participants:
            participants.remove(user_id)
        else:
            participants.append(user_id)

        await state.update_data(participants=participants)
        keyboard = await kb.make_users_as_buttons(callback.from_user.id, participants)
        await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "participants_selected")
async def get_meeting_details(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(WTEXT["request_meeting_details"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_details)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_details))
async def write_event_details(message: Message, state: FSMContext):
    await state.update_data(meeting_details=message.text)

    # Собираем данные из state
    meeting_data = await state.get_data()
    user_tg_id = meeting_data["user_tg_id"]
    meeting_name = meeting_data["meeting_name"]
    meeting_date = meeting_data["meeting_date"]
    meeting_time = convert_str_to_time(meeting_data["meeting_time"])
    meeting_duration = meeting_data["duration"]
    meeting_participants = meeting_data["participants"]
    meeting_details = meeting_data["meeting_details"]

    # Записываем в БД и получаем meeting_id
    meeting_id = await dbm.write_meeting_in_db(
        user_tg_id, meeting_name, meeting_date, meeting_time,
        meeting_duration, meeting_details, meeting_participants
    )

    # Отправляем приглашения
    text_for_send = (f"Вы приглашены на событие: {meeting_name}\n"
                     f"День проведения: {meeting_date}\n"
                     f"Время начала встречи: {meeting_time}\n"
                     f"Встреча займет: {meeting_duration} минут.\n"
                     f"Пожалуйста, подтвердите или отклоните приглашение.")

    for participant in meeting_participants:
        keyboard = await kb.accept_decline_meeting_buttons(participant, meeting_id)
        await message.bot.send_message(chat_id=participant,
                                       text=text_for_send,
                                       reply_markup=keyboard)

    await db.update_statistics(meeting_count=True)
    await message.answer(WTEXT["meeting_made"])
    await state.clear()
