from aiogram import Bot, Dispatcher, F
from aiogram.types import BotCommand, Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage

import keyboards as kb  # модуль с клавиатурами
import lexicon as lx  # модуль с текстами
import secrets  # модуль с токеном бота

BOT_TOKEN = secrets.BOT_TOKEN
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class FSMFillForm(StatesGroup):
    fill_event_name = State()
    fill_event_date = State()
    fill_event_time = State()
    fill_event_details = State()


calendar_bot_app = ''


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
    await state.set_state(FSMFillForm.fill_event_name)


# Хэндлер для неотловленных сообщений
@dp.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)


