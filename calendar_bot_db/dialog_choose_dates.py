import logging
from datetime import date

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar, ManagedCalendar
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import DialogManager, Window

from calendar_bot_db.states import FSMEditEvent, FSMCreateEvent, FSMCreateMeeting
from calendar_bot_db.models import crud_sqla_core as db
from calendar_bot_db.models.config import storage
from calendar_bot_db.lexicon import WARNING_TEXTS as WTEXT
import calendar_bot_db.keyboards as kb

from typing import Optional


logger = logging.getLogger(__name__)


def _make_key(callback: CallbackQuery) -> Optional[StorageKey]:
    try:
        key = StorageKey(bot_id=callback.bot.id,
                         chat_id=callback.message.chat.id,
                         user_id=callback.from_user.id)
        return key
    except Exception as e:
        logger.debug(f"Произошла ошибка в _make_key {e}")
        return None


async def select_event_date(callback: CallbackQuery, widget: ManagedCalendar,
                            manager: DialogManager, timestamp: date) -> None:
    try:
        date_for_show = timestamp.strftime("%d.%m.%Y")

        # Инициализируем контекст для сохранения даты и внесения изменений
        key = _make_key(callback)
        logger.debug(f"key = {key}")
        state = FSMContext(storage=storage, key=key)
        logger.debug(f"state = {state}")
        await state.update_data(event_date=date_for_show)
        await manager.done()

        # Ответ пользователю с выбранной датой
        await callback.answer()  # Подтверждаем получение callback
        await callback.message.answer(f"Вы выбрали: {date_for_show}")

        # Запрашиваем время события, выдаем клавиатуру, меняем state
        await callback.message.answer(WTEXT["request_event_time"],
                                      reply_markup=kb.time_keyboard())
        await state.set_state(FSMCreateEvent.fill_event_time)
    except Exception as e:
        logger.debug(f"Произошла ошибка в select_event_date {e}")
        return None


async def select_meeting_date(callback: CallbackQuery, widget: ManagedCalendar,
                              manager: DialogManager, timestamp: date) -> None:
    try:
        date_for_show = timestamp.strftime("%d.%m.%Y")

        # Инициализируем контекст для сохранения даты и внесения изменений
        key = _make_key(callback)
        logger.debug(f"key = {key}")
        state = FSMContext(storage=storage, key=key)
        logger.debug(f"state = {state}")
        await state.update_data(meeting_date=date_for_show)
        await manager.done()

        # Ответ пользователю с выбранной датой
        await callback.answer()  # Подтверждаем получение callback
        await callback.message.answer(f"Вы выбрали: {date_for_show}")

        # Запрашиваем время события, выдаем клавиатуру, меняем state
        await callback.message.answer(WTEXT["request_meeting_time"],
                                      reply_markup=kb.time_keyboard())
        await state.set_state(FSMCreateMeeting.fill_meeting_time)
    except Exception as e:
        logger.debug(f"Произошла ошибка в select_meeting_date {e}")
        return None


async def edit_date(callback: CallbackQuery, widget: ManagedCalendar,
                    manager: DialogManager, timestamp: date) -> None:
    try:
        date_for_show = timestamp.strftime('%d.%m.%Y')

        # Инициализируем контекст для сохранения даты и внесения изменений
        key = _make_key(callback)
        state = FSMContext(storage=storage, key=key)

        await state.update_data(event_date=timestamp)
        user_data = await state.get_data()
        await manager.done()

        # Ответ пользователю с выбранной датой
        await callback.answer()  # Подтверждаем получение callback
        await callback.message.answer(f"Вы выбрали новую дату: {date_for_show}")

        # Вносим изменения в событие
        await db.change_event(user_data["user_tg_id"], user_data["event_id"],
                              new_event_date=user_data["event_date"])

        # Добавляем в статистику
        await db.update_statistics(edited_events=True)

        # Оповещаем о внесении изменений, обнуляем state
        await callback.message.answer(WTEXT["event_date_edited"])
        await state.clear()
    except Exception as e:
        logger.debug(f"Произошла ошибка в edit_date {e}")
        return None


# Создание виджета календаря
set_event_date = Calendar(id='set_calendar', on_click=select_event_date)
set_meeting_date = Calendar(id='set_calendar', on_click=select_meeting_date)
edit_calendar_date = Calendar(id='edit_calendar', on_click=edit_date)

# Создаем окно календаря
set_calendar_window_for_event = Window(Const(WTEXT["request_event_date"]),
                                       set_event_date, state=FSMCreateEvent.fill_event_date)

set_calendar_window_for_meeting = Window(Const(WTEXT["request_meeting_date"]),
                                         set_meeting_date, state=FSMCreateMeeting.fill_meeting_date)

edit_event_date_calendar_window = Window(Const(WTEXT["request_event_date"]),
                                         edit_calendar_date, state=FSMEditEvent.edit_event_date)
