import logging

from aiogram import Router, F

from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT

from calendar_bot_db.models.crud_meetings import (
    get_calendar_events,
    change_events_visibility,
)
from calendar_bot_db.states import FSMMenuOptions

import calendar_bot_db.keyboards as kb


logger = logging.getLogger(__name__)

router = Router(name="publish_event_router")


@router.message(Command(commands=["12"]), StateFilter(default_state))
async def choose_event_for_publish(message: Message, state: FSMContext):
    user_tg_id = message.from_user.id
    all_events = await get_calendar_events(user_tg_id=user_tg_id, for_callback=True)
    keyboard = await kb.make_events_as_choosen_buttons(all_events=all_events)

    await state.update_data(all_events=all_events, events_to_publish=[])
    await message.answer(text=WTEXT["choose_for_publish"], reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.publish_event)


@router.callback_query(
    F.data != "events_selected", StateFilter(FSMMenuOptions.publish_event)
)
async def choose_event_point_for_edit(callback: CallbackQuery, state: FSMContext):
    storage_data: dict = await state.get_data()
    all_events = storage_data["all_events"]
    if all_events:
        # Выгружаем события для публикации
        events_to_publish: list[str] = storage_data["events_to_publish"]

        # Сохраняем название выбранного события из callback
        choosen_event_name: str = callback.data

        # Если выбранное событие уже в списке, удаляем его, если нет,
        # сохраняем в список, для передачи списка и формированию клавиатуры
        # выбранные события получают метку о выборе в названии
        if choosen_event_name in events_to_publish:
            events_to_publish.remove(choosen_event_name)
        else:
            events_to_publish.append(choosen_event_name)

        await state.update_data(events_to_publish=events_to_publish)
        keyboard = await kb.make_events_as_choosen_buttons(
            events_to_publish=events_to_publish, all_events=all_events
        )
        await callback.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await callback.message.answer("У вас нет доступных событий для публикации.")


@router.callback_query(
    F.data == "events_selected", StateFilter(FSMMenuOptions.publish_event)
)
async def change_event_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем получение callback

    choosen_event_data = await state.get_data()
    events_to_publish = choosen_event_data["events_to_publish"]

    await change_events_visibility(
        callback.from_user.id, events_to_publish, publish=True
    )
    await callback.message.delete_reply_markup()
    await callback.message.delete()
    await callback.message.answer(text=WTEXT["events_published"])
    await state.clear()
