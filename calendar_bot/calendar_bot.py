from aiogram import Bot, Dispatcher, F

from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram_dialog import DialogManager, Window, Dialog, setup_dialogs
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.text import Const

from calendar_async_back import (write_event_in_json_file,  # модуль с бэкэндом
                                 read_event,
                                 format_event_data)
from dialog_funcs import select_date
from states import FSMFillEvent, FSMMenuOptions, storage
import keyboards as kb  # модуль с клавиатурами
import lexicon as lx  # модуль с текстами
import secrets  # модуль с токеном бота

BOT_TOKEN = secrets.BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


# Создание виджета календаря
calendar = Calendar(id='calendar', on_click=select_date)

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


# Забираем дату события, переключаемся на введение details
@dp.callback_query(F.data.startswith("time"), StateFilter(FSMFillEvent.fill_event_time))
async def process_event_date(callback: CallbackQuery, state: FSMContext):
    event_time = callback.data[5:]
    await callback.message.answer(f"Вы выбрали {event_time} временем события.")
    await state.update_data(event_time=event_time)
    await callback.message.answer(lx.WARNING_TEXTS["request_event_details"])
    await state.set_state(FSMFillEvent.fill_event_details)


# Забираем описание и записываем событие в файл
@dp.message(StateFilter(FSMFillEvent.fill_event_details))
async def write_event_details(message: Message, state: FSMContext):
    await state.update_data(details=message.text)

    # Собираем данные из state
    event_data = await state.get_data()
    event_name = event_data["event_name"]
    event_date = event_data["event_date"]
    event_time = event_data["event_time"]
    event_details = event_data["details"]

    # Записываем в файл
    await write_event_in_json_file(event_name, event_date, event_time, event_details)
    await message.answer(lx.WARNING_TEXTS["event_made"])
    await state.clear()


@dp.message(Command(commands=["2"]), StateFilter(default_state))
async def show_event(message: Message, state: FSMContext):
    # Выбираем событие инлайн кнопкой
    keyboard = kb.make_events_as_buttons()
    await message.answer(text=lx.WARNING_TEXTS["request_event_for_show"],
                         reply_markup=keyboard)
    # Переводимся в состояние чтения заметки
    await state.set_state(FSMMenuOptions.read_event)


@dp.callback_query(StateFilter(FSMMenuOptions.read_event))
async def show_requested_event(callback: CallbackQuery, state: FSMContext):
    event_for_read = callback.data
    event_data = await read_event(event_for_read)
    await callback.answer()  # Подтверждаем получение callback
    await callback.message.answer(lx.WARNING_TEXTS["show_event"])
    await callback.message.answer(format_event_data(event_data))
    await state.clear()


@dp.message(Command(commands=["3"]), StateFilter(default_state))
async def choose_event_for_edit(message: Message, state: FSMContext):
    keyboard = kb.make_events_as_buttons()
    await message.answer(text=lx.WARNING_TEXTS["request_event_for_edit"],
                         reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.choose_event)


@dp.callback_query(StateFilter(FSMMenuOptions.choose_event))
async def choose_event_point_for_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=lx.WARNING_TEXTS["request_event_point_for_edit"],
                                  reply_markup=kb.make_event_point_as_buttons())
    await state.set_state(FSMMenuOptions.choose_event_point)


@dp.callback_query(StateFilter(FSMMenuOptions.choose_event_point))
async def change_event_point(callback: CallbackQuery, state: FSMContext):
    ...


# Хэндлер для неотловленных сообщений
@dp.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
