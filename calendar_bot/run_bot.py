# Bot - класс, представляющий бота, отвечает за взаимодействие с telegram
# Dispatcher - класс, который распределяет входищие апдейты по обработчикам
from aiogram import Bot, Dispatcher, F  # экземпляр класса MagicFilter
# Command и CommandStart это фильтры, с помощью которых мы отлавливаем апдейты
# StateFilter - фильтр состояний для работы FSM
from aiogram.filters import Command, CommandStart, StateFilter
# FSMContext класс для хранения контекста, в котором находятся пользователи
from aiogram.fsm.context import FSMContext
# импортируем классы состояний для работы FSM
from aiogram.fsm.state import default_state, State, StatesGroup
# MemoryStorage - класс хранилище данных состояний пользователей для FSM
from aiogram.fsm.storage.memory import MemoryStorage
# Message это объект, содержащий информацию о сообщении в Telegram
# BotCommand для управления командами бота
from aiogram.types import (Message, BotCommand,
                           CallbackQuery,  # тип апдейта
                           InlineKeyboardMarkup,  # объект клавиатуры
                           InlineKeyboardButton,)  # объект инлайн-кнопки
# импортируем токен бота из закрытого файла
from secrets import BOT_TOKEN
# импортируем тексты меню и ответов бота
from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

bot_token = BOT_TOKEN
# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher()


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMWriteNotes(StatesGroup):
    waiting_for_note_name = State()  # Состояние ожидания ввода названия заметки
    waiting_for_note_text = State()  # Состояние ожидания ввода текста заметки


async def set_main_menu(bot: bot):  # функция для настройки меню бота
    main_menu_commands = [BotCommand(command=command, description=description)
                          for command, description in MENU_TEXT.items()]
    await bot.set_my_commands(main_menu_commands)


# Хэндлер для обработки команды start вне состояний
# и предлагать выбрать пункт меню
@dp.message(CommandStart(), StateFilter(default_state))  # регистрируем хендлер
async def process_start_command(message: Message):
    await message.answer(NOTIFICATION_TEXTS['hello'])
    await message.answer(NOTIFICATION_TEXTS['menu'])


# Хэндлер для обработки команды /cancel в состоянии по умолчанию
# и сообщать, что эта команда работает только после выбора п. меню
@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=NOTIFICATION_TEXTS['cancel'])
    await message.answer(NOTIFICATION_TEXTS['menu'])


# Хэндлер для обработки команды /cancel в любых состояниях,
# кроме состояния по умолчанию и отключать FSM
@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=NOTIFICATION_TEXTS['exit'])
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


# Хэндлер для обработки команды help
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(NOTIFICATION_TEXTS['help'])
    await message.answer(NOTIFICATION_TEXTS['menu'])


# Хэндлер для обработки команды меню 1: Создать заметку
@dp.message(Command(commands=['1']), StateFilter(default_state))
async def process_create_note(message: Message, state: FSMContext):
    await message.answer(text=NOTIFICATION_TEXTS['new_note_name'])
    # Устанавливаем состояние ожидания ввода названия заметки
    await state.set_state(FSMWriteNotes.waiting_for_note_name)
    # Устанавливаем состояние ожидания ввода текста заметки
    await state.set_state(FSMWriteNotes.waiting_for_note_text)

if __name__ == '__main__':
    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)
    # Запускаем long polling опрос сервера на апдейты
    dp.run_polling(bot)

