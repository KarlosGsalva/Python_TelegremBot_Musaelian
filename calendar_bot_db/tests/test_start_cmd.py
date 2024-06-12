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

user_id = 123421
chat_id = 123421
text_incoming_user_message = "/start"
text_start_first_bot_answer = "Здравствуйте, для начала работы выберите пункт меню:"
text_start_second_bot_answer = (
    "/start: Начать работу\n"
    "/1: Создать событие\n"
    "/2: Вывести подробности события\n"
    "/3: Изменить данные события\n"
    "/4: Удалить событие\n"
    "/5: Показать все события\n"
    "/6: Регистрация\n"
    "/7: Создать встречу\n"
    "/8: Показать назначенные встречи\n"
    "/9: Удалить встречу\n"
    "/10: Показать календарь\n"
    "/11: Поделиться событием\n"
    "/12: Опубликовать события\n"
    "/13: Показать публичные события\n"
    "/14: Выгрузить события в json\n"
    "/15: Выгрузить события в csv"
)
text_check_calendar_widget = "Пожалуйста, выберите дату события"


@pytest.mark.asyncio
async def test_cmd_start(dp, bot):
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
            message_id=2,
            date=datetime.now(),
            chat=chat,
            text=text_start_first_bot_answer,
        ),
    )

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=Message(
            message_id=3,
            date=datetime.now(),
            chat=chat,
            text=text_start_second_bot_answer,
        ),
    )

    user_message = Message(
        message_id=1,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text=text_incoming_user_message,
    )

    result = await dp.feed_update(bot, Update(message=user_message, update_id=1))
    assert result is not UNHANDLED

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_start_first_bot_answer

    outgoing_message: TelegramType = bot.get_request()
    print(f"type outgoing_message: ", type(outgoing_message))
    print(f"outgoing_message: ", outgoing_message.__dict__)
    print("outgoing_message_text:", outgoing_message.text)
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == text_start_second_bot_answer
