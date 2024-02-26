from aiogram import Bot, Dispatcher, F

from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, Window, Dialog, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Calendar
from aiogram_dialog.widgets.text import Const

# from calendar_async_back import on_date_selected  # модуль с бэкэндом
import keyboards as kb  # модуль с клавиатурами
import lexicon as lx  # модуль с текстами
import secrets  # модуль с токеном бота
from datetime import date

BOT_TOKEN = secrets.BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class FSMFillEvent(StatesGroup):
    fill_event_name = State()
    fill_event_date = State()
    fill_event_time = State()
    fill_event_details = State()


class FSMMenuOptions(StatesGroup):
    read_event = State()
    edit_event = State()
    delete_event = State()


async def on_date_selected(callback: CallbackQuery, widget,
                           manager: DialogManager,
                           timestamp: date):
    timestamp = int(callback.data[callback.data.find(':') + 1:])
    manager.dialog_data['event_date'] = date.fromtimestamp(timestamp)
    date_for_show = manager.dialog_data['event_date'].strftime('%d.%m.%Y')
    key = StorageKey(bot_id=callback.bot.id,
                     chat_id=callback.message.chat.id,
                     user_id=callback.from_user.id)
    state = FSMContext(storage=storage, key=key)
    await manager.done()
    # Ответ пользователю с выбранной датой
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(f"Вы выбрали: {date_for_show}")
    await callback.message.answer(lx.WARNING_TEXTS["request_event_time"])
    await state.set_state(FSMFillEvent.fill_event_time)

# Создание виджета календаря
calendar = Calendar(id='calendar', on_click=on_date_selected)


# calendar_bot_app = ''

# Пишем окно календаря
calendar_window = Window(Const(lx.WARNING_TEXTS["request_event_date"]),
                         calendar, state=FSMFillEvent.fill_event_date)

# Регистрируем окно в диалоге, диалог в диспетчере
dialog = Dialog(calendar_window)
dp.include_router(dialog)
# Инициализация DialogManager
setup_dialogs(dp)


# Устанавливаем меню бота
async def set_main_menu(bot: bot):
    main_menu_commands = [BotCommand(command=command, description=description)
                          for command, description in lx.MENU.items()]
    await bot.set_my_commands(main_menu_commands)


# Обрабатываем команду старт, выдаем меню
@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(lx.WARNING_TEXTS["hello"])
    await message.answer(lx.WARNING_TEXTS["show_menu"])


# Обрабатываем команду cancel на дефолтном state
@dp.message(Command(commands=["cancel"]), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(lx.WARNING_TEXTS["cancel"])


# Обрабатываем callback cancel: отмены, на не дефолтном state
@dp.callback_query(F.data == "cancel", ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=lx.WARNING_TEXTS["exit"])
    await callback.answer()
    await state.clear()


# Обрабатываем команду /1: Создать событие
@dp.message(Command(commands=["1"]), StateFilter(default_state))
async def create_event(message: Message, state: FSMContext):
    await message.answer(lx.WARNING_TEXTS["request_event_name"],
                         reply_markup=kb.cancel_markup)
    await state.set_state(FSMFillEvent.fill_event_name)


# Забираем название события, переключаемся на введение даты
@dp.message(StateFilter(FSMFillEvent.fill_event_name))
async def process_event_name(message: Message, state: FSMContext,
                             dialog_manager: DialogManager):
    await state.update_data(event_name=message.text)
    # отправляем календарь
    await dialog_manager.start(FSMFillEvent.fill_event_date)


# Забираем дату события, переключаемся на введение времени
@dp.message(StateFilter(FSMFillEvent.fill_event_time))
async def process_event_date(message: Message, state: FSMContext):
    await state.update_data(event_time=message.text)
    await state.set_state(FSMFillEvent.fill_event_details)


# Хэндлер для неотловленных сообщений
@dp.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)


