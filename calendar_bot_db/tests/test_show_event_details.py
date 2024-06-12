import asyncio
from datetime import datetime

import pytest
import sys

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, User, Message

# для устранения несовместимости ProactorEventLoop в Windows и библиотекой psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

user_id = 123418
chat_id = 123418
text_incoming_user_2_cmd = "/2"
text_bot_query_event_name = "Пожалуйста, выберите событие для чтения:"


@pytest.mark.asyncio
async def test_cmd_2_show_event_details(dp, bot):
    chat = Chat(id=chat_id, type=ChatType.PRIVATE)
    user = User(id=user_id, is_bot=False, first_name="User")

    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot, user_id=user_id, chat_id=chat_id
    )
    await fsm_context.clear()

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=7,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_query_event_name,
        ),
    )

    user_message_cmd_2 = Message(
        message_id=8,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_2_cmd,
    )

    cmd_2_result = await dp.feed_update(
        bot, Update(message=user_message_cmd_2, update_id=3)
    )
    assert cmd_2_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_query_event_name
