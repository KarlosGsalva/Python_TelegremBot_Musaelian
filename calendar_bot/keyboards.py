from aiogram.utils.keyboard import (InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)


# Создаем инлайн кнопку cancel
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


# Создаем клавиатуру для выбора времени
def time_keyboard():
    times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)]
    buttons = [InlineKeyboardButton(text=time, callback_data=f"time:{time}") for time in times]
    buttons.append(cancel_button)
    return buttons


def make_inline_keyboard():
    ikb_builder = InlineKeyboardBuilder()
    buttons = time_keyboard()
    ikb_builder.row(*buttons, width=4)
    return ikb_builder.as_markup()

