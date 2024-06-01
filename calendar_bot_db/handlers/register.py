import logging

from aiogram import Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from calendar_bot_db.models import crud_events as db
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb
from calendar_bot_db.states import FSMRegistryUser

logger = logging.getLogger(__name__)

router = Router(name="show_events_router")


@router.message(Command(commands=["6"]), StateFilter(default_state))
async def registry_user(message: Message, state: FSMContext):
    await message.answer(WTEXT["request_username"])
    await state.set_state(FSMRegistryUser.fill_username)


@router.message(StateFilter(FSMRegistryUser.fill_username))
async def get_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(WTEXT["request_email"])
    await state.set_state(FSMRegistryUser.fill_email)


@router.message(StateFilter(FSMRegistryUser.fill_email))
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(WTEXT["request_password"])
    await state.set_state(FSMRegistryUser.fill_password)


@router.message(StateFilter(FSMRegistryUser.fill_password))
async def save_user_data(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await db.save_registry_user_data(user_tg_id=message.from_user.id,
                                     username=user_data["username"],
                                     user_email=user_data["email"],
                                     user_password=message.text)
    await message.answer(WTEXT["data_saved"])
    await state.clear()
