import logging

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.types import Message

from calendar_bot_db.models.crud_meetings import get_user_busy_slots


logger = logging.getLogger(__name__)

router = Router(name="show_user_meetings_router")


@router.message(Command(commands=["8"]), StateFilter(default_state))
async def get_user_events(message: Message):
    user_tg_id = message.from_user.id
    meetings_schedule = await get_user_busy_slots(user_tg_id)
    await message.answer(meetings_schedule)
