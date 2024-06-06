import asyncio
from datetime import datetime
import pytest
import sys

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage, EditMessageReplyMarkup
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, User, Message, CallbackQuery

# для устранения несовместимости ProactorEventLoop в Windows и библиотекой psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

text_incoming_user_10_cmd = "/10"
text_bot_show_meetings_details = ("Для просмотра календаря в браузере, нажмите на кнопку\n "
                                  "'Мой календарь'и перейдите по ссылке.\n\n"
                                  "Для получения расписания в чате, нажмите на кнопку "
                                  "'Вывести расписание в чат'")


@pytest.mark.asyncio
async def test_cmd_10_show_user_calendar(dp, bot):
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=21,
            date=datetime.now(),
            chat=Chat(id=1234567, type=ChatType.PRIVATE),
            text=text_bot_show_meetings_details,
        ),
    )

    user_message_cmd_10 = Message(message_id=22,
                                  date=datetime.now(),
                                  chat=chat,
                                  from_user=user,
                                  text=text_incoming_user_10_cmd)

    cmd_10_result = await dp.feed_update(bot, Update(message=user_message_cmd_10, update_id=10))
    assert cmd_10_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_show_meetings_details
