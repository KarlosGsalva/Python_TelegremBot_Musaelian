import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

logger = logging.getLogger(__name__)

router = Router(name="start_cmd_router")


# Обрабатываем команду старт, выдаем меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(WTEXT["hello"])
    await message.answer(WTEXT["show_menu"])


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


# Хэндлер для неотловленных сообщений
@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")


# Хэндлер для неотловленных callback
@router.callback_query(StateFilter(default_state))
async def echo(callback: CallbackQuery):
    await callback.message.answer(text="Извините, я вас не понимать")
    await callback.answer()
