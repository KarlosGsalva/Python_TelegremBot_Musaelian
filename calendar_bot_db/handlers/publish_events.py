import json
import logging

from aiogram import Router, F
from aiogram_dialog import DialogManager
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
from calendar_bot_db.models import crud_events as db
from calendar_bot_db.models.crud_events import gather_user_or_events_db
from calendar_bot_db.models.crud_meetings import get_calendar_events, change_event_visibility
from calendar_bot_db.states import FSMMenuOptions

import calendar_bot_db.keyboards as kb

from calendar_bot_db.services import split_callback_to_name_id, convert_str_to_time

logger = logging.getLogger(__name__)

router = Router(name="publish_event_router")


@router.message(Command(commands=["12"]), StateFilter(default_state))
async def choose_event_for_publish(message: Message, state: FSMContext):
    # Выгружаем все события пользователя
    events_data: list[dict] = await get_calendar_events(message.from_user.id, for_keyboard=True)
    keyboard = await kb.make_events_as_choosen_buttons(message.from_user.id)

    # Сохраняем события в storage
    logger.debug(f"events_data в choose_event_for_publish = {events_data}")

    await state.update_data(events=events_data, events_to_publish=[])
    await message.answer(text=WTEXT["choose_for_publish"], reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.publish_event)


@router.callback_query(F.data != "events_selected", StateFilter(FSMMenuOptions.publish_event))
async def choose_event_point_for_edit(callback: CallbackQuery, state: FSMContext):
    storage_data: dict = await state.get_data()

    # Выгружаем события для публикации
    events_to_publish: list[str] = storage_data["events_to_publish"]

    # Сохраняем название выбранного события из callback
    choosen_event_name: str = callback.data

    # Если выбранное событие уже в списке, удаляем его, если нет,
    # сохраняем в список, для передачи списка и формированию клавиатуры
    # выбранные события получают метку в названии
    if choosen_event_name in events_to_publish:
        events_to_publish.remove(choosen_event_name)
    else:
        events_to_publish.append(choosen_event_name)
    # ---------------
    logger.debug(f"storage_data =  {storage_data}")
    logger.debug(f"events_to_publish =  {events_to_publish}")
    logger.debug(f"choosen_event_name =  {choosen_event_name}")
    # ---------------
    await state.update_data(events_to_publish=events_to_publish)
    keyboard = await kb.make_events_as_choosen_buttons(callback.from_user.id, events_to_publish)
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@router.callback_query(F.data == "events_selected", StateFilter(FSMMenuOptions.publish_event))
async def change_event_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем получение callback

    choosen_event_data = await state.get_data()
    logger.debug(f"choosen_event_data in change_event_name = {choosen_event_data}")
    for event in choosen_event_data["events_to_publish"]:
        logger.debug(f"event in 'for event in choosen_event_data['events_to_publish']:' =  {event}")
        await change_event_visibility(callback.from_user.id, event, publish=True)
    await callback.message.answer(text=WTEXT["events_published"])
    await state.clear()


