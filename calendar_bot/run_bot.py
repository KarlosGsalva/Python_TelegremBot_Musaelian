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
                           InlineKeyboardButton, )  # объект инлайн-кнопки
# импортируем бэкенд приложения
import async_notesapp
# импортируем тексты меню и ответов бота
from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS
# импортируем токен бота из закрытого файла
from secrets import BOT_TOKEN
# импортируем клавиатуры
import keyboards as kb

# Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
storage = MemoryStorage()

bot_token = BOT_TOKEN
# Создаем объекты бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(storage=MemoryStorage())

# Создаем экземляр класса AsyncNotesApp
notes_app = async_notesapp.AsyncNotesApp()


# Создадим 'базу данных' для избежания потери данных
# т.к. MemoryStorage зависим от оперативной памяти
# notes_dict: dict[str | int, str] = {}


# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMWriteNotes(StatesGroup):
    waiting_for_note_name = State()  # Состояние ожидания ввода названия заметки
    waiting_for_note_text = State()  # Состояние ожидания ввода текста заметки
    waiting_for_note_delete = State()  # Состояние ожидания названия заметки для удаления


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
@dp.callback_query(F.data == 'cancel',
                   ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=NOTIFICATION_TEXTS['exit'])
    # Подтверждаем получение callback, чтобы кнопка не подсвечивалась
    await callback.answer()
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
    await message.answer(text=NOTIFICATION_TEXTS['request_note_name'],
                         reply_markup=kb.cancel_markup)
    # Устанавливаем состояние ожидания ввода названия заметки
    await state.set_state(FSMWriteNotes.waiting_for_note_name)


# Хэндлер для проверки введения названия заметки и перевода
# в состояние ожидания ввода текста заметки
@dp.message(StateFilter(FSMWriteNotes.waiting_for_note_name))
async def process_note_name(message: Message, state: FSMContext):
    # Сохраняем данные внутри контекста асинх. методом update_data()
    # на случай отмены ввода
    await state.update_data(name=message.text)
    await message.answer(text=NOTIFICATION_TEXTS['request_note_text'],
                         reply_markup=kb.cancel_markup)
    # Устанавливаем состояние ввода текста заметки
    await state.set_state(FSMWriteNotes.waiting_for_note_text)


# Хэндлер для обработки введения некорректного названия заметки
@dp.message(StateFilter(FSMWriteNotes.waiting_for_note_name))
async def warning_note_name(message: Message):
    await message.answer(text=NOTIFICATION_TEXTS['incorrect_note_name'],
                         reply_markup=kb.cancel_markup)


# Хэндлер для обработки введения текста заметки
@dp.message(StateFilter(FSMWriteNotes.waiting_for_note_text))
async def process_note_text(message: Message, state: FSMContext):
    # Сохраняем текст заметки в хранилище по ключу text

    await state.update_data(text=message.text)

    # Вытаскиваем данные для создания заметки
    user_data = await state.get_data()
    note_name = user_data['name']
    note_text = user_data['text']

    # Создаем заметку
    await notes_app.create_note(note_name=note_name, note_text=note_text)
    await message.answer(NOTIFICATION_TEXTS['note_created'])
    await state.set_state(default_state)


# Хэндлер для обработки команды меню 4: Удалить заметку
@dp.message(Command(commands=['4']), StateFilter(default_state))
async def process_delete_note(message: Message, state: FSMContext):
    await message.answer(text=NOTIFICATION_TEXTS['choose_for_delete'],
                         reply_markup=kb.cancel_markup)
    # Устанавливаем состояние ожидания ввода названия заметки
    await state.set_state(FSMWriteNotes.waiting_for_note_delete)


# Хэндлер для всех неотловленных сообщений
@dp.message(StateFilter(default_state))
async def echo(message: Message):
    await message.reply(text='Извините, я вас не понимать')


if __name__ == '__main__':
    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)
    # Запускаем long polling опрос сервера на апдейты
    dp.run_polling(bot)
