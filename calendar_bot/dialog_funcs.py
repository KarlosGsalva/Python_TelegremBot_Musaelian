from datetime import date

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from states import FSMMenuOptions, FSMFillEvent, storage
import lexicon as lx
import keyboards as kb


async def select_date(callback: CallbackQuery, widget,
                      manager: DialogManager,
                      timestamp: date):
    timestamp = int(callback.data[callback.data.find(':') + 1:])
    manager.dialog_data['event_date'] = date.fromtimestamp(timestamp)
    date_for_show = manager.dialog_data['event_date'].strftime('%d.%m.%Y')

    key = StorageKey(bot_id=callback.bot.id,
                     chat_id=callback.message.chat.id,
                     user_id=callback.from_user.id)
    state = FSMContext(storage=storage, key=key)
    await state.update_data(event_date=date_for_show)
    await manager.done()
    # Ответ пользователю с выбранной датой
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(f"Вы выбрали: {date_for_show}")
    await callback.message.answer(lx.WARNING_TEXTS["request_event_time"],
                                  reply_markup=kb.make_inline_keyboard())
    await state.set_state(FSMFillEvent.fill_event_time)