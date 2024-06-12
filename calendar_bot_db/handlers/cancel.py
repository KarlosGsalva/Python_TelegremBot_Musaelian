import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

logger = logging.getLogger(__name__)

router = Router(name="start_cmd_router")


# Обрабатываем команду cancel на дефолтном state
@router.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(WTEXT["cancel"])


# Обрабатываем команду cancel на дефолтном state
@router.callback_query(F.data == "cancel", StateFilter(default_state))
async def process_cancel_callback_command(callback: CallbackQuery):
    await callback.message.answer(WTEXT["cancel"])
    await callback.answer()


# Обрабатываем callback cancel: отмены, на не дефолтном state
@router.callback_query(F.data == "cancel", ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=WTEXT["exit"])
    await callback.answer()
    await state.clear()
