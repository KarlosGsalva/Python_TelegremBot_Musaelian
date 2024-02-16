from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup)
import async_notesapp as an
import asyncio


async def _make_inline_buttons() -> list:
    buttons: list[InlineKeyboardButton] = []
    files = await asyncio.to_thread(lambda: an.AsyncNotesApp.gather_all_notes())
    for note in files:
        button = InlineKeyboardButton(text=f"Удалить {note}", callback_data=f"delete_{note}")
        buttons.append(button)
    buttons.append(InlineKeyboardButton(text='отмена', callback_data='cancel'))
    return buttons


async def delete_notes_keyboard():
    # инициализируем билдер для формирования клавиатуры
    ikb_builder = InlineKeyboardBuilder()
    buttons = await _make_inline_buttons()
    ikb_builder.row(*buttons, width=1)
    return ikb_builder.as_markup()

# Создаем inline кнопку cancel
cancel_button = InlineKeyboardButton(text='отмена', callback_data='cancel')
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)









