import logging

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery


logger = logging.getLogger(__name__)

router = Router(name="start_cmd_router")


# Хэндлер для неотловленных сообщений
@router.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")


# Хэндлер для неотловленных callback
@router.callback_query(StateFilter(default_state))
async def echo(callback: CallbackQuery):
    await callback.message.answer(text="Извините, я вас не понимать")
    await callback.answer()
