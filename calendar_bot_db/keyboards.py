import logging

from aiogram.utils.keyboard import (InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)

from calendar_bot_db.models import crud_sqla_core as db
from calendar_bot_db.models import crud_meetings as dbm
from typing import Optional

from calendar_bot_db.models.crud_meetings import gather_all_users_db

logger = logging.getLogger(__name__)

# Создаем инлайн кнопку cancel
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
keyboard: list[list[InlineKeyboardButton]] = [[cancel_button]]
cancel_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
participants_selected_btn = InlineKeyboardButton(text="Участники выбраны", callback_data="participants_selected")


# Создаем клавиатуру
def _make_inline_keyboard(buttons: list[InlineKeyboardButton],
                          width=4) -> Optional[InlineKeyboardMarkup]:
    try:
        ikb_builder = InlineKeyboardBuilder()
        ikb_builder.row(*buttons, width=width)
        return ikb_builder.as_markup()
    except Exception as e:
        logger.debug(f"Произошла ошибка в _make_inline_keyboard {e}")
        return None


# Создаем кнопки для выбора времени
def time_keyboard() -> Optional[InlineKeyboardMarkup]:
    try:
        times = [f"{hour:02d}:{minute:02d}" for hour in range(24) for minute in (0, 15, 30, 45)]
        buttons = [InlineKeyboardButton(text=time, callback_data=f"time:{time}") for time in times]
        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons)
    except Exception as e:
        logger.debug(f"Произошла ошибка в time_keyboard {e}")
        return None


# Создаем события как кнопки
async def make_events_as_buttons(user_tg_id: int) -> Optional[InlineKeyboardMarkup]:
    try:
        buttons: list[InlineKeyboardButton] = []
        events: dict = await db.gather_all_events_db(user_tg_id)

        for detail in events.values():
            button = InlineKeyboardButton(text=detail["event_name"],
                                          callback_data=f"{detail['event_name']}__{detail['id']}")
            buttons.append(button)

        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_events_as_buttons {e}")
        return None


# Создаем пункты события как кнопки
def make_event_points_as_buttons() -> Optional[InlineKeyboardMarkup]:
    try:
        buttons = [InlineKeyboardButton(text="Название события", callback_data=f"change_event_name"),
                   InlineKeyboardButton(text="Дата события", callback_data=f"change_event_date"),
                   InlineKeyboardButton(text="Время события", callback_data=f"change_event_time"),
                   InlineKeyboardButton(text="Описание события", callback_data=f"change_event_details"),
                   cancel_button]
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_event_point_as_buttons {e}")
        return None


async def make_users_as_buttons(user_tg_id, selected_participants: list = None
                                ) -> Optional[InlineKeyboardMarkup]:
    try:
        all_participants = await gather_all_users_db(user_tg_id=user_tg_id)
        buttons = []

        if selected_participants is not None:
            for user_id, user in all_participants.items():
                text = f"{user['username ✔️']}" if user_id in selected_participants else f"{user['username']}"
                buttons.append(InlineKeyboardButton(text=text, callback_data=user_id))
        else:
            for user_id, user in all_participants.items():
                buttons.append(InlineKeyboardButton(text=f"{user['username']}",
                                                    callback_data=user['user_id']))

        buttons.append(participants_selected_btn)
        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_users_as_buttons {e}")
        return None
