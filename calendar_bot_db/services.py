import logging
from typing import Optional

from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand, InlineKeyboardMarkup

from bcrypt import hashpw, gensalt
from datetime import time

logger = logging.getLogger(__name__)


def is_number(num):
    try:
        return int(num)
    except Exception as e:
        logger.debug(f"Произошла ошибка в is_number = {e}")
        return False


def convert_str_to_time(chosen_time: str):
    try:
        new_event_time = time(*[int(tm) for tm in chosen_time.split(":")])
        return new_event_time
    except Exception as e:
        logger.debug(f"Произошла ошибка в convert_str_to_time = {e}")
        return None


def split_callback_to_name_id(callback: str) -> Optional[dict]:
    try:
        name, id = callback.split("__")
        return {"name": name, "id": int(id)}
    except Exception as e:
        logger.debug(f"Произошла ошибка в split_callback_to_name_id = {e}")
        return None


def hash_password(password: str) -> str:
    password = password.encode("utf-8")
    salt = gensalt()
    return hashpw(password, salt).decode("utf-8")


def inline_keyboards_are_different(kb1: InlineKeyboardMarkup, kb2: InlineKeyboardMarkup) -> bool:
    if len(kb1.inline_keyboard) != len(kb2.inline_keyboard):
        return True
    for row1, row2 in zip(kb1.inline_keyboard, kb2.inline_keyboard):
        if len(row1) != len(row2):
            return True
        for button1, button2 in zip(row1, row2):
            if button1.text != button2.text or button1.callback_data != button2.callback_data:
                logger.debug(f"Button1: {button1.text}, {button1.callback_data}")
                logger.debug(f"Button2: {button2.text}, {button2.callback_data}")
                return True
    return False


def make_dict_to_str(dictionary: dict):
    try:
        return "\n".join(f"{k}: {v}" for k, v in dictionary.items())
    except Exception as e:
        logger.debug(f"Произошла ошибка в make_dict_to_str {e}")
        return None


async def set_main_menu_cmds(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="1", description="Создать событие"),
        BotCommand(command="2", description="Вывести подробности события"),
        BotCommand(command="3", description="Изменить данные события"),
        BotCommand(command="4", description="Удалить событие"),
        BotCommand(command="5", description="Показать все события"),
        BotCommand(command="6", description="Регистрация"),
        BotCommand(command="7", description="Создать встречу"),
        BotCommand(command="8", description="Показать список встреч"),
        BotCommand(command="9", description="Удалить встречу"),
        BotCommand(command="10", description="Показать мой календарь"),
        BotCommand(command="11", description="Поделиться событием"),
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )


