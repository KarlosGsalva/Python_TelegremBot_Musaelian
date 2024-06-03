import json
import logging

from aiogram import Router, F
from aiogram_dialog import DialogManager
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_events as db
from calendar_bot_db.models.crud_events import gather_user_or_events_db
from calendar_bot_db.models.crud_meetings import get_calendar_events, change_events_visibility
from calendar_bot_db.states import FSMMenuOptions

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import split_callback_to_name_id, convert_str_to_time

logger = logging.getLogger(__name__)

router = Router(name="show_published_events_router")


@router.message(Command(commands=["13"]), StateFilter(default_state))
async def choose_event_for_publish(message: Message):
    user_tg_id = message.from_user.id
    all_events = await get_calendar_events(user_tg_id=user_tg_id, publish=True)
    if all_events:
        await message.answer(text=WTEXT["show_published_events"])
        await message.answer(text=all_events)
    else:
        await message.answer("В данный момент нет открытых событий.")
