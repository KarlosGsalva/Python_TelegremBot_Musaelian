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

text_incoming_user_3_cmd = "/3"
text_bot_query_event_for_edit = "Выберите событие для изменения:"


@pytest.mark.asyncio
async def test_cmd_2_show_event_details(dp, bot):
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=8,
            date=datetime.now(),
            chat=Chat(id=1234567, type=ChatType.PRIVATE),
            text=text_bot_query_event_for_edit,
        ),
    )

    user_message_cmd_3 = Message(message_id=9,
                                 date=datetime.now(),
                                 chat=chat,
                                 from_user=user,
                                 text=text_incoming_user_3_cmd)

    cmd_3_result = await dp.feed_update(bot, Update(message=user_message_cmd_3, update_id=4))
    assert cmd_3_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_query_event_for_edit

