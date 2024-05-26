import logging

from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram_dialog import DialogManager

from calendar_bot_db.models import crud_sqla_core as db
from calendar_bot_db.models import crud_meetings as dbm
from calendar_bot_db.services import convert_str_to_time, inline_keyboards_are_different
from calendar_bot_db.states import FSMCreateMeeting
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

import calendar_bot_db.keyboards as kb


logger = logging.getLogger(__name__)

router = Router(name="create_meeting_router")


# Хэндлер для создания встречи
@router.message(Command(commands=["7"]), StateFilter(default_state))
async def create_meeting(message: Message, state: FSMContext):
    await message.answer(WTEXT["request_meeting_name"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_name)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_name))
async def get_meeting_name(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await state.update_data(user_tg_id=message.from_user.id)
    await state.update_data(meeting_name=message.text)
    await dialog_manager.start(FSMCreateMeeting.fill_meeting_date)


@router.callback_query(F.data.startswith("time"), StateFilter(FSMCreateMeeting.fill_meeting_time))
async def set_meeting_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    meeting_time = callback.data[5:]
    await callback.message.answer(f"Вы выбрали {meeting_time} временем встречи.")
    await state.update_data(meeting_time=meeting_time)
    await callback.message.answer(WTEXT["request_meeting_duration"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_duration)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_duration))
async def set_meeting_duration(message: Message, state: FSMContext):
    duration = message.text

    if duration.isdigit():
        await message.answer(f"Планируемое время встречи {duration} минут.")
        await state.update_data(duration=duration, participants=[])
        keyboard = await kb.make_users_as_buttons(message.from_user.id)
        await message.answer(WTEXT["request_meeting_participants"], reply_markup=keyboard)
        await state.set_state(FSMCreateMeeting.fill_meeting_participants)
    else:
        await message.answer(WTEXT["duration_warning"])
        await message.answer(WTEXT["request_meeting_details"], reply_markup=kb.cancel_markup)


@router.callback_query(StateFilter(FSMCreateMeeting.fill_meeting_participants))
async def get_participants(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.debug(f"data = {data}")
    user_id = callback.data.replace("user_", "")

    logger.debug(f"data['participants'] на входе = {data['participants']}")
    if user_id in data["participants"]:
        data["participants"].remove(user_id)
        logger.debug(f"data['participants'] на выходе = {data['participants']}")
    else:
        data["participants"].append(user_id)
        logger.debug(f"data['participants'] добавлен пользователь = {data['participants']}")

    await state.update_data(participants=data["participants"])
    keyboard = await kb.make_users_as_buttons(callback.from_user.id, data["participants"])
    # await callback.message.edit_reply_markup(reply_markup=keyboard)

    # Проверяем, изменилось ли содержимое
    current_keyboard = callback.message.reply_markup

    if keyboard and current_keyboard:
        if inline_keyboards_are_different(keyboard, current_keyboard):
            await callback.message.edit_reply_markup(reply_markup=keyboard)
        else:
            logger.debug("Содержимое и разметка не изменились, обновление не требуется.")
    else:
        await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "participants_selected")
async def get_meeting_details(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(WTEXT["request_meeting_details"], reply_markup=kb.cancel_markup)
    await state.set_state(FSMCreateMeeting.fill_meeting_details)


@router.message(StateFilter(FSMCreateMeeting.fill_meeting_details))
async def write_event_details(message: Message, state: FSMContext):
    await state.update_data(meeting_details=message.text)

    # Собираем данные из state
    meeting_data = await state.get_data()
    user_tg_id = meeting_data["user_tg_id"]
    meeting_name = meeting_data["meeting_name"]
    meeting_date = meeting_data["meeting_date"]
    meeting_time = convert_str_to_time(meeting_data["meeting_time"])
    meeting_duration = meeting_data["duration"]
    meeting_participants = meeting_data["participants"]
    meeting_details = meeting_data["meeting_details"]

    # Записываем в БД
    await dbm.write_meeting_in_db(user_tg_id, meeting_name, meeting_date, meeting_time,
                                  meeting_duration, meeting_details, meeting_participants)
    await db.update_statistics(event_count=True)
    await message.answer(WTEXT["meeting_made"])
    await state.clear()

