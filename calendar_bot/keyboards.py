from aiogram.utils.keyboard import (InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)


# Создаем инлайн кнопку cancel
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


