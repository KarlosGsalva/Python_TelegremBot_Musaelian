from aiogram.utils.keyboard import (InlineKeyboardBuilder,
                                    InlineKeyboardButton,
                                    InlineKeyboardMarkup)
import async_notesapp
import asyncio

from constant_texts import NOTIFICATION_TEXTS

# Создаем inline кнопку cancel
cancel_button = InlineKeyboardButton(text='отмена', callback_data='cancel')
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

# Создаем экземпляр класса AsyncNotesApp
async_notes_app = async_notesapp.AsyncNotesApp()


async def _make_callback_inline_buttons(mode: str) -> list | None:
    try:
        buttons: list[InlineKeyboardButton] = []
        files = await asyncio.to_thread(lambda: async_notes_app.gather_all_notes())
        # Создаем кнопки в зависимости от mode'а
        if mode == 'show_sorted_notes':
            buttons = await async_notes_app.notes_in_inline_buttons()
            return buttons
        if mode == 'show_notes':
            buttons = await async_notes_app.notes_in_inline_buttons(False)
            return buttons
        for note in files:
            if mode == 'delete':
                button = InlineKeyboardButton(text=f"Удалить {note[:-9]}", callback_data=f"delete_{note}")
            elif mode == 'read':
                button = InlineKeyboardButton(text=f"Прочитать {note[:-9]}", callback_data=f"read_{note}")
            elif mode == 'edit':
                button = InlineKeyboardButton(text=f"Редактировать {note[:-9]}", callback_data=f"edit_{note}")
            if button is not None:
                buttons.append(button)
        buttons.append(cancel_button)
        return buttons
    except Exception as e:
        print(NOTIFICATION_TEXTS['error'], e)


async def make_notes_as_inline_buttons(mode: str):
    try:
        # инициализируем билдер для формирования клавиатуры
        ikb_builder = InlineKeyboardBuilder()
        # создаем кнопки и добавляем в билдер
        buttons = await _make_callback_inline_buttons(mode)
        ikb_builder.row(*buttons, width=1)
        return ikb_builder.as_markup()
    except Exception as e:
        print(NOTIFICATION_TEXTS['error'], e)
        return cancel_markup









