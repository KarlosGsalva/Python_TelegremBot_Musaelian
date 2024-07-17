import asyncio
import logging
from datetime import datetime
import pytest
import sys

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, User, Message

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# для устранения несовместимости ProactorEventLoop в Windows и библиотекой psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

user_id = 123421
chat_id = 123421
text_incoming_user_13_cmd = "/13"
text_bot_share_event = "Пожалуйста, открытые события:"


@pytest.mark.asyncio
async def test_cmd_13_show_public_events(dp, bot):
    chat = Chat(id=chat_id, type=ChatType.PRIVATE)
    user = User(id=user_id, is_bot=False, first_name="new_user")

    fsm_context: FSMContext = dp.fsm.get_context(
        bot=bot, user_id=user_id, chat_id=chat_id
    )
    await fsm_context.clear()

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=30,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_share_event,
        ),
    )

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=30,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_share_event,
        ),
    )

    user_message_cmd_13 = Message(
        message_id=29,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_13_cmd,
    )

    cmd_13_result = await dp.feed_update(
        bot, Update(message=user_message_cmd_13, update_id=13)
    )
    assert cmd_13_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_share_event
