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

from calendar_bot_db.states import FSMMenuOptions

# для устранения несовместимости ProactorEventLoop в Windows и библиотекой psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

user_id = 12345678
chat_id = 12345678
text_incoming_user_4_cmd = "/4"
text_bot_query_event_for_delete = "Выберите событие для удаления:"


@pytest.mark.asyncio
async def test_cmd_4_choose_event_for_delete(dp, bot):
    chat = Chat(id=chat_id, type=ChatType.PRIVATE)
    user = User(id=user_id, is_bot=False, first_name="User")

    fsm_context: FSMContext = dp.fsm.get_context(bot=bot, user_id=user_id, chat_id=chat_id)
    await fsm_context.clear()

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=8,
            date=datetime.now(),
            chat=Chat(id=chat_id, type=ChatType.PRIVATE),
            text=text_bot_query_event_for_delete,
        ),
    )

    user_message_cmd_4 = Message(message_id=9,
                                 date=datetime.now(),
                                 chat=chat,
                                 from_user=user,
                                 text=text_incoming_user_4_cmd)


    cmd_4_result = await dp.feed_update(bot, Update(message=user_message_cmd_4, update_id=4))
    assert cmd_4_result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    current_state = await fsm_context.get_state()
    print(f"type outgoing_message:", type(outgoing_message))
    print(f"outgoing_message:", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    print("current_state:", current_state)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_bot_query_event_for_delete
    assert current_state == FSMMenuOptions.delete_event
