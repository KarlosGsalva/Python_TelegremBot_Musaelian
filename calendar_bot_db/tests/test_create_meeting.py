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

user_id = 123459
chat_id = 123459
text_incoming_user_7_cmd = "/7"
text_bot_create_meeting = "Пожалуйста, введите название новой встречи:"


@pytest.mark.asyncio
async def test_cmd_7_create_meeting(dp, bot):
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
            message_id=13,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_create_meeting,
        ),
    )

    user_message_cmd_7 = Message(
        message_id=14,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_7_cmd,
    )

    cmd_7_result = await dp.feed_update(
        bot, Update(message=user_message_cmd_7, update_id=14)
    )
    assert cmd_7_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    current_state = await fsm_context.get_state()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    print("current_state:", current_state)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_create_meeting
