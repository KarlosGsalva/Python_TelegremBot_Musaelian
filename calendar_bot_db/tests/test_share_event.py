import asyncio
from datetime import datetime
import pytest
import sys

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, EditMessageReplyMarkup
from aiogram.methods.base import TelegramType
from aiogram.types import Update, Chat, User, Message, CallbackQuery

# для устранения несовместимости ProactorEventLoop в Windows и библиотекой psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

user_id = 123416
chat_id = 123416
text_incoming_user_11_cmd = "/11"
text_bot_share_event = "Пожалуйста, выберие событие которым хотите поделиться:"


@pytest.mark.asyncio
async def test_cmd_11_share_event(dp, bot):
    chat = Chat(id=chat_id, type=ChatType.PRIVATE)
    user = User(id=user_id, is_bot=False, first_name="User")

    fsm_context: FSMContext = dp.fsm.get_context(bot=bot, user_id=user_id, chat_id=chat_id)
    await fsm_context.clear()

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=25,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_share_event,
        ),
    )

    user_message_cmd_11 = Message(message_id=26,
                                  date=datetime.now(),
                                  chat=chat,
                                  from_user=user,
                                  text=text_incoming_user_11_cmd)

    cmd_11_result = await dp.feed_update(bot, Update(message=user_message_cmd_11, update_id=11))
    assert cmd_11_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_share_event
