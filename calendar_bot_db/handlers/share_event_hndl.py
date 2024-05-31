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
from calendar_bot_db.services import make_dict_to_str
from calendar_bot_db.states import FSMMenuOptions
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb

from datetime import datetime as dt, timedelta

logger = logging.getLogger(__name__)

router = Router(name="share_event_router")


# Хэндлер отправки встречи выбранным пользователям
@router.message(Command(commands=["11"]), StateFilter(default_state))
async def create_meeting(message: Message, state: FSMContext):
    events_data: dict = await dbm.get_calendar_events(message.from_user.id, for_callback=True)
    logger.debug(f"events_data = {events_data}\n")

    keyboard = await kb.make_events_meetings_as_buttons(events_data)
    logger.debug(f"keyboard in create_meeting = {keyboard}\n")

    await state.update_data(events_data, participants=[])
    await message.answer(WTEXT["share_event"], reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.choice_for_share)


@router.callback_query(F.data.startswith("event_btn_"), StateFilter(FSMMenuOptions.choice_for_share))
async def get_meeting_name(callback: CallbackQuery, state: FSMContext):
    user_tg_id = callback.from_user.id
    data = await state.get_data()
    keyboard = await kb.make_users_as_buttons(user_tg_id)

    event_key = callback.data.replace("event_btn_", "")
    logger.debug(f"event_key = {event_key}")
    logger.debug(f"data = {data}")
    logger.debug(f"data[event_key] = {data[event_key]}")

    choosen_event_details = make_dict_to_str(data[event_key])
    logger.debug(f"choosen_event_details = {choosen_event_details}")

    await state.update_data(event=event_key, choosen_event_details=choosen_event_details)
    await callback.message.answer(text=WTEXT["request_shared_participant"], reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.choose_participant)


@router.callback_query(F.data != "participants_selected", StateFilter(FSMMenuOptions.choose_participant))
async def chose_participant(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    participants = data["participants"]
    user_id = callback.data

    if user_id in participants:
        participants.remove(user_id)
    else:
        participants.append(user_id)
    logger.debug(f"participants = {participants}")

    await state.update_data(participants=participants)
    keyboard = await kb.make_users_as_buttons(callback.from_user.id, participants)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "participants_selected", StateFilter(FSMMenuOptions.choose_participant))
async def send_choosen_event(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.debug(f"callback.data in send_choosen_event = {callback.data}")

    participants = data["participants"]
    for member in participants:
        await callback.bot.send_message(text=data["choosen_event_details"], chat_id=member)
    await callback.message.answer("Событие отправлено")
    await state.clear()
