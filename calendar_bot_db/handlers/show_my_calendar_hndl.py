import logging

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.types import Message

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models.config import settings

import calendar_bot_db.keyboards as kb


logger = logging.getLogger(__name__)

router = Router(name="show_calendar_router")
NGROK_URL = settings.NGROK_URL


# Хэндлер для показа всех событий
@router.message(Command(commands=["9"]), StateFilter(default_state))
async def show_all_events(message: Message):
    calendar_url = f"{NGROK_URL}calendar/?id={message.from_user.id}"
    keyboard = await kb.make_url_link_button(calendar_url)
    await message.answer(WTEXT["calendar"],
                         reply_markup=keyboard)
