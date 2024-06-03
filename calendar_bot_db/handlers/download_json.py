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

router = Router(name="download_json_router")
NGROK_URL = settings.NGROK_URL


# Хэндлер для показа всех событий
@router.message(Command(commands=["14"]), StateFilter(default_state))
async def show_all_events(message: Message):
    json_link_url = f"{NGROK_URL}export/json/?id={message.from_user.id}"
    button_text = "Просмотреть данные в json"
    callback_data = "show_json"
    keyboard = await kb.make_url_link_button(button_text, json_link_url, callback_data)
    await message.answer(WTEXT["watch_json"], reply_markup=keyboard)
