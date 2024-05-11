from aiogram import Bot, F

from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram_dialog import DialogManager, Dialog, setup_dialogs

from async_file_back import (write_event_in_json_file,  # модуль с бэкэндом
                             read_event, change_event_point,
                             format_event_data, delete_event)
from calendar_bot_db.models.config import settings
from dialog_choose_dates import set_calendar_window, edit_calendar_window
from states import FSMCreateEvent, FSMEditEvent, FSMMenuOptions, dp
import keyboards as kb  # модуль с клавиатурами
import lexicon as lx  # модуль с текстами


BOT_TOKEN = settings.bot_token.get_secret_value()
bot = Bot(token=BOT_TOKEN)

# Регистрируем окно в диалоге, диалог в диспетчере
dialog_create_state = Dialog(set_calendar_window)
dialog_edit_state = Dialog(edit_calendar_window)
dp.include_router(dialog_create_state)
dp.include_router(dialog_edit_state)
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


# Обрабатываем команду cancel на дефолтном state
@dp.callback_query(F.data == "cancel", StateFilter(default_state))
async def process_cancel_callback_command(callback: CallbackQuery):
    await callback.message.answer(lx.WARNING_TEXTS["cancel"])
    await callback.answer()


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
    await state.set_state(FSMCreateEvent.fill_event_name)


# Забираем название события, переключаемся на введение даты
@dp.message(StateFilter(FSMCreateEvent.fill_event_name))
async def process_event_name(message: Message, state: FSMContext,
                             dialog_manager: DialogManager):
    await state.update_data(event_name=message.text)
    # отправляем календарь
    await dialog_manager.start(FSMCreateEvent.fill_event_date)


# Забираем дату события, переключаемся на введение details
@dp.callback_query(F.data.startswith("time"), StateFilter(FSMCreateEvent.fill_event_time))
async def process_event_date(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с time
    event_time = callback.data[5:]
    await callback.message.answer(f"Вы выбрали {event_time} временем события.")
    await state.update_data(event_time=event_time)
    await callback.message.answer(lx.WARNING_TEXTS["request_event_details"])
    await state.set_state(FSMCreateEvent.fill_event_details)


# Забираем описание и записываем событие в файл
@dp.message(StateFilter(FSMCreateEvent.fill_event_details))
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
    await state.set_state(FSMEditEvent.choose_event)


@dp.callback_query(StateFilter(FSMEditEvent.choose_event))
async def choose_event_point_for_edit(callback: CallbackQuery, state: FSMContext):
    event_name = callback.data[:-5]
    await state.update_data(event_name=event_name)
    await callback.message.answer(text=lx.WARNING_TEXTS["request_event_point_for_edit"],
                                  reply_markup=kb.make_event_point_as_buttons())
    await callback.answer()
    await state.set_state(FSMEditEvent.choose_event_point)


@dp.callback_query(F.data == "change_event_date", StateFilter(FSMEditEvent.choose_event_point))
async def get_new_event_date(callback: CallbackQuery, state: FSMContext,
                             dialog_manager: DialogManager):
    await dialog_manager.start(FSMEditEvent.edit_event_date)


@dp.callback_query(F.data == "change_event_time", StateFilter(FSMEditEvent.choose_event_point))
async def get_new_event_time(callback: CallbackQuery, state: FSMContext):
    keyboard = kb.time_keyboard()
    await callback.message.answer(text=lx.WARNING_TEXTS["request_new_event_time"],
                                  reply_markup=keyboard)
    await state.set_state(FSMEditEvent.edit_event_time)


@dp.callback_query(F.data.startswith("time"), StateFilter(FSMEditEvent.edit_event_time))
async def edit_event_time(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с time
    new_event_time = callback.data[5:]  # сохраняем время без "time"

    # Сохраняем данные из state
    user_data = await state.get_data()

    # Изменяем событие
    await change_event_point(user_data["event_name"], "Время события",
                             new_event_time)

    # Уведомляем об успешном изменении данных
    await callback.message.answer(text=f"Новое время события: {new_event_time}")
    await callback.message.answer(lx.WARNING_TEXTS["event_time_edited"])
    await state.clear()


# Хэндлер 4 пункта меню, удалить событие
@dp.callback_query(F.data == "change_event_details", StateFilter(FSMEditEvent.choose_event_point))
async def request_new_event_details(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с выбором опции
    await callback.message.answer(lx.WARNING_TEXTS["request_new_event_details"])
    await state.set_state(FSMEditEvent.edit_event_details)


# Хэндлер меняющий описание выбранного события
@dp.message(StateFilter(FSMEditEvent.edit_event_details))
async def set_new_event_details(message: Message, state: FSMContext):
    # Сохраняем новое описание события
    new_event_details = message.text

    # Сохраняем данные из state
    user_data = await state.get_data()

    # Изменяем событие
    await change_event_point(user_data["event_name"], "Описание события",
                             new_event_details)

    # Уведомляем об успешном изменении данных
    await message.answer(text=f"Новое описание события: {new_event_details}")
    await message.answer(lx.WARNING_TEXTS["event_details_edited"])
    await state.clear()


# Хэндлер 4 пункта меню, удалить событие
@dp.message(Command(commands=["4"]), StateFilter(default_state))
async def request_event_for_delete(message: Message, state: FSMContext):
    keyboard = kb.make_events_as_buttons()
    await message.answer(text=lx.WARNING_TEXTS["request_event_for_delete"],
                         reply_markup=keyboard)
    await state.set_state(FSMMenuOptions.delete_event)


# Хэндлер для удаления выбранного события
@dp.callback_query(StateFilter(FSMMenuOptions.delete_event))
async def make_delete_event(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # подтверждаем получение callback с выбором события
    await delete_event(callback.data)
    await callback.message.answer(text=f"Событие {callback.data[:-5]} удалено.")
    await state.clear()


# Хэндлер для показа всех событий
@dp.message(Command(commands=["5"]), StateFilter(default_state))
async def show_all_events(message: Message):
    keyboard = kb.make_events_as_buttons()
    await message.answer(lx.WARNING_TEXTS["show_all_events"],
                         reply_markup=keyboard)


# Хэндлер для неотловленных сообщений
@dp.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")


# Хэндлер для неотловленных callback
@dp.callback_query(StateFilter(default_state))
async def echo(callback: CallbackQuery):
    await callback.message.answer(text="Извините, я вас не понимать")
    await callback.answer()


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
