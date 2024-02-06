# Bot - класс, представляющий бота, отвечает за взаимодействие с telegram
# Dispatcher - класс, который распределяет входищие апдейты по обработчикам
from aiogram import Bot, Dispatcher
# Command и CommandStart это фильтры, с помощью которых мы отлавливаем апдейты
from aiogram.filters import Command, CommandStart
# Message это объект, содержащий информацию о сообщении в Telegram
# BotCommand для управления командами бота
from aiogram.types import Message, BotCommand
# импортируем токен бота из закрытого файла
from secrets import BOT_TOKEN
# импортируем тексты меню и ответов бота
from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS

bot_token = BOT_TOKEN
# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()


async def set_main_menu(bot: bot):  # функция для настройки меню бота
    main_menu_commands = [BotCommand(command=command, description=description)
                          for command, description in MENU_TEXT.items()]
    await bot.set_my_commands(main_menu_commands)


# хэндлер для обработки команды start
@dp.message(CommandStart())  # регистрируем хендлер
async def process_start_command(message: Message):
    menu_text = "\n".join(f"{key}: {value}" for key, value in MENU_TEXT.items())
    await message.answer(NOTIFICATION_TEXTS['hello'])
    await message.answer(menu_text)


# хэндлер для обработки команды help
@dp.message(Command(commands=['help']))  # регистрируем хендлер
async def process_help_command(message: Message):
    await message.answer(NOTIFICATION_TEXTS['help'])


if __name__ == '__main__':
    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)
    # Запускаем long polling опрос сервера на апдейты
    dp.run_polling(bot)

