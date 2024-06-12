import logging

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.types import Message

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb


logger = logging.getLogger(__name__)

router = Router(name="show_events_router")


# Хэндлер для показа всех событий
@router.message(Command(commands=["5"]), StateFilter(default_state))
async def show_all_events(message: Message):
    keyboard = await kb.make_events_as_buttons(message.from_user.id)
    await message.answer(WTEXT["show_all_events"], reply_markup=keyboard)
