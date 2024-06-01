import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models.crud_events import check_or_create_exists_user

logger = logging.getLogger(__name__)

router = Router(name="start_cmd_router")


# Обрабатываем команду старт, выдаем меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    user_tg_id = message.from_user.id
    await check_or_create_exists_user(user_tg_id)
    await message.answer(WTEXT["hello"])
    await message.answer(WTEXT["show_menu"])


# Обрабатываем команду старт, выдаем меню
@router.message(CommandStart(), ~StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WTEXT["hello"])
    await message.answer(WTEXT["show_menu"])
