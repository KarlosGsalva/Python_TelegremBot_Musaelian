import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models.config import settings

import calendar_bot_db.keyboards as kb
from calendar_bot_db.models.crud_meetings import get_calendar_events

logger = logging.getLogger(__name__)

router = Router(name="show_calendar_router")
NGROK_URL = settings.NGROK_URL


# Хэндлер для показа всех событий
@router.message(Command(commands=["10"]), StateFilter(default_state))
async def show_all_events(message: Message):
    calendar_url = f"{NGROK_URL}calendar/?id={message.from_user.id}"
    button_text = "Мой календарь"
    callback_data = "show_calendar"

    keyboard = await kb.make_url_link_button(
        button_text, calendar_url, callback_data, schedule_button=True
    )
    await message.answer(WTEXT["calendar"], reply_markup=keyboard)


@router.callback_query(F.data == "show_calendar")
async def show_full_calendar(callback: CallbackQuery):
    await callback.answer()
    user_tg_id = callback.from_user.id
    text = await get_calendar_events(user_tg_id)
    await callback.message.answer(text=text)
