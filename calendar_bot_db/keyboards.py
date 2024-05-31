import logging

from aiogram.utils.keyboard import (InlineKeyboardButton,
                                    InlineKeyboardMarkup,
                                    InlineKeyboardBuilder)

from calendar_bot_db.models import crud_events as db
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
        events: dict = await db.gather_user_events_db(user_tg_id)

        for detail in events.values():
            button = InlineKeyboardButton(text=detail["event_name"],
                                          callback_data=f"{detail['event_name']}__{detail['id']}")
            buttons.append(button)

        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_events_as_buttons {e}")
        return None


async def make_meetings_as_buttons(user_tg_id: int) -> Optional[InlineKeyboardMarkup]:
    try:
        buttons: list[InlineKeyboardButton] = []
        meetings: dict = await dbm.gather_user_meetings_db(user_tg_id)

        for detail in meetings.values():
            logger.debug(f"detail В make_meetings_as_buttons = {detail}")
            button = InlineKeyboardButton(text=detail["meeting_name"],
                                          callback_data=f"{detail['meeting_name']}__{detail['id']}")
            buttons.append(button)

        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_meetings_as_buttons {e}")
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
        logger.debug(f"All participants: {all_participants}")
        buttons = []

        if all_participants is None:
            return None

        if selected_participants is not None:
            for user in all_participants.values():
                is_selected = user["user_id"] in selected_participants
                text = f"{user['username']} ✔️" if is_selected else f"{user['username']}"
                callback_data = user["user_id"]

                logger.debug(f"User ID: {user['user_id']}, "
                             f"Text: {text}, "
                             f"Callback Data: {callback_data}, "
                             f"Is selected: {is_selected}")
                buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        else:
            for user_id, user in all_participants.items():
                callback_data = user['user_id']
                buttons.append(InlineKeyboardButton(text=f"{user['username']}",
                                                    callback_data=callback_data))

        buttons.append(participants_selected_btn)
        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_users_as_buttons {e}")
        return None


async def accept_decline_meeting_buttons(participant_id, meeting_id):
    try:
        accept_btn = InlineKeyboardButton(
            text="Принять",
            callback_data=f"accepted_by_{participant_id}_meeting_{meeting_id}"
        )
        decline_btn = InlineKeyboardButton(
            text="Отклонить",
            callback_data=f"declined_by_{participant_id}_meeting_{meeting_id}"
        )
        return _make_inline_keyboard([accept_btn, decline_btn, cancel_button])
    except Exception as e:
        logger.debug(f"Произошла ошибка в accept_decline_meeting_buttons {e}")
        return None


async def make_url_link_button(calendar_url):
    try:
        login_btn = InlineKeyboardButton(text="Мой календарь", url=calendar_url)
        calendar_btn = InlineKeyboardButton(text="Вывести расписание в чат", callback_data="show_calendar")
        return _make_inline_keyboard([login_btn, calendar_btn])
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_url_login_button {e}")
        return None


async def make_events_meetings_as_buttons(events_data: dict):
    try:
        buttons: list[InlineKeyboardButton] = []
        logger.debug(f"events_data in make_events_meetings_as_buttons = {events_data}")

        for event in events_data:
            logger.debug(f"event in for event in events_data: = {event}")

            text = events_data[event]["name"]
            logger.debug(f"text in for event in events_data: = {events_data[event]['name']}")

            callback_data = f"event_btn_{events_data[event]['name']}"
            logger.debug(f"callback_data in for event in events_data: = {callback_data}")

            buttons.append(InlineKeyboardButton(text=text, callback_data=callback_data))
            logger.debug(f"event buttons in make_events_meetings_as_buttons = {buttons}")

        buttons.append(cancel_button)
        return _make_inline_keyboard(buttons=buttons, width=1)
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_events_meetings_as_buttons {e}")
        return None
