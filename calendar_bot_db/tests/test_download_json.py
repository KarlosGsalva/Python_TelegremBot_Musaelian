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

user_id = 123413
chat_id = 123413
text_incoming_user_14_cmd = "/14"
text_bot_download_json = "Для просмотра json перейдите по ссылке, нажав на кнопку:"


@pytest.mark.asyncio
async def test_cmd_14_download_json(dp, bot):
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
            message_id=31,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_download_json,
        ),
    )

    user_message_cmd_14 = Message(
        message_id=32,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_14_cmd,
    )

    cmd_14_result = await dp.feed_update(
        bot, Update(message=user_message_cmd_14, update_id=14)
    )
    assert cmd_14_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_download_json
