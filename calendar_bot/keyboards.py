from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup)
from os import listdir, path

# инициализируем билдер для формирования клавиатуры
ikb_builder = InlineKeyboardBuilder()


# собираем список заметок из текущей директории
# если директория не указана
def _gather_all_notes(main_path=None) -> list:
    try:
        if main_path is None:
            main_path = path.dirname(__file__)
        return [note for note in listdir(main_path) if note.endswith('note.txt')]
    except Exception as e:
        print('Произошла ошибка', e)


def _make_inline_buttons() -> list:
    buttons: list[InlineKeyboardButton] = []
    for note in _gather_all_notes():
        button = InlineKeyboardButton(text=f"Удалить {note}", callback_data='delete_button')
        buttons.append(button)
    return buttons


# Создаем inline кнопку cancel
cancel_button = InlineKeyboardButton(text='отмена', callback_data='cancel')
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

ikb_builder.row(*_make_inline_buttons())








