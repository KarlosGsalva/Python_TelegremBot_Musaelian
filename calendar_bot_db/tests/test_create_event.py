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

from calendar_bot_db.states import FSMCreateEvent

# для устранения несовместимости ProactorEventLoop в Windows и библиотекой psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

user_id = 123410
chat_id = 123410
text_incoming_user_1_cmd = "/1"
text_incoming_user_event_name = "random text"
text_bot_query_event_name = "Пожалуйста, введите название нового события:"
text_bot_query_event_date = "Пожалуйста, выберите дату события:"


@pytest.mark.asyncio
async def test_cmd_1_create_event(dp, bot):
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
            message_id=6,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_query_event_name,
        ),
    )

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=7,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_query_event_date,
        ),
    )

    user_message_cmd_1 = Message(
        message_id=4,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_1_cmd,
    )

    user_message_event_name = Message(
        message_id=5,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_event_name,
    )

    cmd_1_result = await dp.feed_update(
        bot, Update(message=user_message_cmd_1, update_id=2)
    )
    assert cmd_1_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    current_state = await fsm_context.get_state()
    print("type outgoing_message:", type(outgoing_message))
    # print("outgoing_message:", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    print("current_state:", current_state)
    assert isinstance(outgoing_message, SendMessage)
    assert current_state == FSMCreateEvent.fill_event_name

    cmd_event_name = await dp.feed_update(
        bot, Update(message=user_message_event_name, update_id=3)
    )
    assert cmd_event_name is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    current_state = await fsm_context.get_state()
    print("type outgoing_message:", type(outgoing_message))
    # print("outgoing_message:", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    print("current_state:", current_state)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_query_event_date
