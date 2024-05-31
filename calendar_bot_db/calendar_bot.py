import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram_dialog import Dialog, setup_dialogs

from calendar_bot_db.dialog_choose_dates import (set_calendar_window_for_event,
                                                 edit_event_date_calendar_window,
                                                 set_calendar_window_for_meeting)
from calendar_bot_db.models.config import settings, storage
from calendar_bot_db.handlers import (start_cmd_hdlrs, show_event_detail, show_events_hndl,
                                      register_hdlr, create_event_hndl, edit_event_hndl,
                                      delete_event_hndl, cancel_hdlrs, end_cap_hndl,
                                      create_meeting_hndl, accept_decline_hndl, show_user_meetings,
                                      show_my_calendar_hndl, delete_meeting_hndl, share_event_hndl)


from colorlog import ColoredFormatter

from calendar_bot_db.services import set_main_menu_cmds

# ------ настройка логов ---------

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    reset=True,
    log_colors={
        'DEBUG': 'yellow',
        'INFO': 'green',
        'WARNING': 'cyan',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={})

for handler in logging.root.handlers:
    handler.setFormatter(color_formatter)

logger = logging.getLogger(__name__)

# ---------------

BOT_TOKEN = settings.bot_token.get_secret_value()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


@dp.startup()
async def on_startup() -> None:
    # Регистрируем окно в диалоге, диалог в диспетчере
    dialog_date_event_state = Dialog(set_calendar_window_for_event)
    dialog_date_meeting_state = Dialog(set_calendar_window_for_meeting)
    dialog_edit_date_state = Dialog(edit_event_date_calendar_window)
    dp.include_router(dialog_date_event_state)
    dp.include_router(dialog_date_meeting_state)
    dp.include_router(dialog_edit_date_state)

    # Инициализация DialogManager
    setup_dialogs(dp)

    # Регистрируем роутеры
    dp.include_router(start_cmd_hdlrs.router)
    dp.include_router(cancel_hdlrs.router)
    dp.include_router(share_event_hndl.router)
    dp.include_router(show_my_calendar_hndl.router)
    dp.include_router(delete_meeting_hndl.router)
    dp.include_router(show_user_meetings.router)
    dp.include_router(accept_decline_hndl.router)
    dp.include_router(create_meeting_hndl.router)
    dp.include_router(show_events_hndl.router)
    dp.include_router(show_event_detail.router)
    dp.include_router(register_hdlr.router)
    dp.include_router(create_event_hndl.router)
    dp.include_router(edit_event_hndl.router)
    dp.include_router(delete_event_hndl.router)
    dp.include_router(end_cap_hndl.router)

    # Установка команд основного меню бота
    await set_main_menu_cmds(bot=bot)


async def main():
    logger.debug(f"{10 * '-'} START {10 * '-'}")
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug(f"{10 * '-'} KeyboardInterrupt {10 * '-'}")
        exit()
