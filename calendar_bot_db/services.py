import logging

from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand, InlineKeyboardMarkup

from bcrypt import hashpw, gensalt
from datetime import time

logger = logging.getLogger(__name__)


def is_number(num):
    try:
        return int(num)
    except Exception as e:
        logger.debug(f"Вместо длительности в минутах введено неверное значение {e}")
        return False


def convert_str_to_time(chosen_time: str):
    new_event_time = time(*[int(tm) for tm in chosen_time.split(":")])
    return new_event_time


def split_callback_to_name_id(callback: str) -> dict:
    event_name, event_id = callback.split("__")
    return {"event_name": event_name, "event_id": int(event_id)}


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
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )


