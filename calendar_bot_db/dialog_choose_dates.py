from datetime import date

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar, ManagedCalendar
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import DialogManager, Window, Dialog, setup_dialogs

from states import FSMEditEvent, FSMCreateEvent, storage, dp
from async_db_back import change_event_point
import lexicon as lx
import keyboards as kb


def _make_key(callback: CallbackQuery) -> StorageKey | None:
    try:
        key = StorageKey(bot_id=callback.bot.id,
                         chat_id=callback.message.chat.id,
                         user_id=callback.from_user.id)
        return key
    except Exception as e:
        print(f"Произошла ошибка{e}")
        return None


async def select_date(callback: CallbackQuery, widget: ManagedCalendar,
                      manager: DialogManager, timestamp: date) -> None:
    try:
        date_for_show = timestamp.strftime('%d.%m.%Y')

        # Инициализируем контекст для сохранения даты и внесения изменений
        key = _make_key(callback)
        state = FSMContext(storage=storage, key=key)
        await state.update_data(event_date=timestamp)
        await manager.done()

        # Ответ пользователю с выбранной датой
        await callback.answer()  # Подтверждаем получение callback
        await callback.message.answer(f"Вы выбрали: {date_for_show}")

        # Запрашиваем время события, выдаем клавиатуру, меняем state
        await callback.message.answer(lx.WARNING_TEXTS["request_event_time"],
                                      reply_markup=kb.time_keyboard())
        await state.set_state(FSMCreateEvent.fill_event_time)
    except Exception as e:
        print(f"Произошла ошибка{e}")
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
        await change_event_point(user_data["event_name"], "Дата события",
                                 user_data["event_date"])

        # Оповещаем о внесении изменений, обнуляем state
        await callback.message.answer(lx.WARNING_TEXTS["event_date_edited"])
        await state.clear()
    except Exception as e:
        print(f"Произошла ошибка{e}")
        return None

# Создание виджета календаря
set_calendar_date = Calendar(id='set_calendar', on_click=select_date)
edit_calendar_date = Calendar(id='edit_calendar', on_click=edit_date)

# Создаем окно календаря
set_calendar_window = Window(Const(lx.WARNING_TEXTS["request_event_date"]),
                             set_calendar_date, state=FSMCreateEvent.fill_event_date)

edit_calendar_window = Window(Const(lx.WARNING_TEXTS["request_event_date"]),
                              edit_calendar_date, state=FSMEditEvent.edit_event_date)

