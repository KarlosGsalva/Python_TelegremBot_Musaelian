from aiogram.utils.keyboard import (InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)

from calendar_async_back import gather_having_events


# Создаем инлайн кнопку cancel
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)


# Создаем клавиатуру
def _make_inline_keyboard(buttons: list[InlineKeyboardButton],
                          width=4) -> InlineKeyboardMarkup | None:
    try:
        ikb_builder = InlineKeyboardBuilder()
        ikb_builder.row(*buttons, width=width)
        return ikb_builder.as_markup()
    except Exception as e:
        print(f"Произошла ошибка{e}")
        return None


# Создаем кнопки для выбора времени
def time_keyboard() -> InlineKeyboardMarkup | None:
    try:
        times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 15, 30, 45)]
        buttons = [InlineKeyboardButton(text=time, callback_data=f"time:{time}") for time in times]
        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons)
    except Exception as e:
        print(f"Произошла ошибка{e}")
        return None


# Создаем события как кнопки
def make_events_as_buttons() -> InlineKeyboardMarkup | None:
    try:
        buttons = [InlineKeyboardButton(text=event_name[:-5], callback_data=f"{event_name}")
                   for event_name in gather_having_events()]
        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        print(f"Произошла ошибка{e}")
        return None


# Создаем пункты события как кнопки
def make_event_point_as_buttons() -> InlineKeyboardMarkup | None:
    try:
        buttons = [InlineKeyboardButton(text="Дата события", callback_data=f"change_event_date"),
                   InlineKeyboardButton(text="Время события", callback_data=f"change_event_time"),
                   InlineKeyboardButton(text="Описание события", callback_data=f"change_event_details"),
                   cancel_button]
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        print(f"Произошла ошибка{e}")
        return None
