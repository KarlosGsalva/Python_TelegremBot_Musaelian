from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage

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


# Хэндлер для неотловленных сообщений
@dp.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text="Извините, я вас не понимать")

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)


