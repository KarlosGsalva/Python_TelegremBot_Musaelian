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

user_id = 123417
chat_id = 123417
text_incoming_user_5_cmd = "/5"
text_bot_show_events = "Пожалуйста, все доступные события:"


@pytest.mark.asyncio
async def test_cmd_5_show_events(dp, bot):
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
            message_id=9,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_show_events,
        ),
    )

    user_message_cmd_5 = Message(
        message_id=10,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_5_cmd,
    )

    cmd_5_result = await dp.feed_update(
        bot, Update(message=user_message_cmd_5, update_id=5)
    )
    assert cmd_5_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_show_events
