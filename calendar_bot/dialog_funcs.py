from datetime import date

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar, ManagedCalendar
from aiogram_dialog.widgets.text import Const
from aiogram_dialog import DialogManager, Window, Dialog, setup_dialogs

from states import FSMMenuOptions, FSMFillEvent, storage, dp
from calendar_async_back import change_event_point
import lexicon as lx
import keyboards as kb


def _make_key(callback: CallbackQuery):
    key = StorageKey(bot_id=callback.bot.id,
                     chat_id=callback.message.chat.id,
                     user_id=callback.from_user.id)
    return key


def _get_date_from_timestamp(callback: CallbackQuery):
    return int(callback.data[callback.data.find(':') + 1:])


async def select_date(callback: CallbackQuery, widget: ManagedCalendar,
                      manager: DialogManager, timestamp: date):
    date_for_show = timestamp.strftime('%d.%m.%Y')

    # Инициализируем контекст для сохранения даты и внесения изменений
    key = _make_key(callback)
    state = FSMContext(storage=storage, key=key)
    await state.update_data(event_date=date_for_show)
    await manager.done()

    # Ответ пользователю с выбранной датой
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(f"Вы выбрали: {date_for_show}")

    # Запрашиваем время события, выдаем клавиатуру, меняем state
    await callback.message.answer(lx.WARNING_TEXTS["request_event_time"],
                                  reply_markup=kb.make_inline_keyboard())
    await state.set_state(FSMFillEvent.fill_event_time)


async def edit_date(callback: CallbackQuery, widget: ManagedCalendar,
                    manager: DialogManager, timestamp: date):
    date_for_show = timestamp.strftime('%d.%m.%Y')
    print(date_for_show)

    # Инициализируем контекст для сохранения даты и внесения изменений
    key = _make_key(callback)
    state = FSMContext(storage=storage, key=key)

    await state.update_data(event_date=date_for_show)
    user_data = await state.get_data()
    print(user_data.items())
    await manager.done()

    # Ответ пользователю с выбранной датой
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(f"Вы выбрали новую дату: {date_for_show}")
    await state.set_state(FSMMenuOptions.set_new_event_date)

    # Вносим изменения в событие
    await change_event_point(user_data["event_name"], "Дата события",
                             user_data["event_date"])

    # Оповещаем о внесении изменений, обнуляем state
    await callback.message.answer(lx.WARNING_TEXTS["event_date_edited"])
    await state.clear()

# Создание виджета календаря
set_calendar_date = Calendar(id='set_calendar', on_click=select_date)
edit_calendar_date = Calendar(id='edit_calendar', on_click=edit_date)

# Создаем окно календаря
set_calendar_window = Window(Const(lx.WARNING_TEXTS["request_event_date"]),
                             set_calendar_date, state=FSMFillEvent.fill_event_date)

edit_calendar_window = Window(Const(lx.WARNING_TEXTS["request_event_date"]),
                              edit_calendar_date, state=FSMMenuOptions.edit_event_date)

