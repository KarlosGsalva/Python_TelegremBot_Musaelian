import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram_dialog import Dialog, setup_dialogs

from calendar_bot_db.dialog_choose_dates import (set_calendar_window_for_event,
                                                 edit_event_date_calendar_window,
                                                 set_calendar_window_for_meeting)
from calendar_bot_db.models.config import settings, storage
from calendar_bot_db.handlers import (start_cmds, show_event, show_events,
                                      register, create_event, edit_event,
                                      delete_event, cancel, end_cap,
                                      create_meeting, accept_decline, show_user_meetings,
                                      show_my_calendar, delete_meeting, share_event,
                                      publish_events, show_published_events, download_json,
                                      download_csv)


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
    dp.include_router(start_cmds.router)
    dp.include_router(cancel.router)
    dp.include_router(download_json.router)
    dp.include_router(download_csv.router)
    dp.include_router(show_published_events.router)
    dp.include_router(publish_events.router)
    dp.include_router(share_event.router)
    dp.include_router(show_my_calendar.router)
    dp.include_router(delete_meeting.router)
    dp.include_router(show_user_meetings.router)
    dp.include_router(accept_decline.router)
    dp.include_router(create_meeting.router)
    dp.include_router(show_events.router)
    dp.include_router(show_event.router)
    dp.include_router(register.router)
    dp.include_router(create_event.router)
    dp.include_router(edit_event.router)
    dp.include_router(delete_event.router)
    dp.include_router(end_cap.router)

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
