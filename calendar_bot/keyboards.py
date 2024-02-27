from aiogram.utils.keyboard import (InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)

from calendar_async_back import gather_having_events


# Создаем инлайн кнопку cancel
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


# Создаем кнопки для выбора времени
def time_keyboard():
    times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 30)]
    buttons = [InlineKeyboardButton(text=time, callback_data=f"time:{time}") for time in times]
    buttons.append(cancel_button)
    return buttons


# Создаем клавиатуру для выбора времени
def make_inline_keyboard(buttons=None, width=4):
    ikb_builder = InlineKeyboardBuilder()
    if buttons is None:
        buttons = time_keyboard()
    ikb_builder.row(*buttons, width=width)
    return ikb_builder.as_markup()


# Создаем события как кнопки
def make_events_as_buttons():
    buttons = [InlineKeyboardButton(text=event_name[:-5], callback_data=f"{event_name}")
               for event_name in gather_having_events()]
    buttons.append(cancel_button)
    return make_inline_keyboard(buttons, width=1)
