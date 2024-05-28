import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from calendar_bot_db.models import crud_sqla_core as db
from calendar_bot_db.models import crud_meetings as dbm
from calendar_bot_db.models.crud_meetings import get_user_busy_slots
from calendar_bot_db.services import convert_str_to_time
from calendar_bot_db.states import FSMCreateMeeting
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb


logger = logging.getLogger(__name__)

router = Router(name="show_user_meetings_router")


@router.message(Command(commands=["8"]), StateFilter(default_state))
async def get_user_events(message: Message):
    user_tg_id = message.from_user.id
    meetings_schedule = await get_user_busy_slots(user_tg_id)
    await message.answer(meetings_schedule)
