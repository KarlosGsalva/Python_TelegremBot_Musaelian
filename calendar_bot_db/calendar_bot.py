import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.methods import DeleteWebhook
from aiogram_dialog import Dialog, setup_dialogs

from calendar_bot_db.dialog_choose_dates import set_calendar_window, edit_calendar_window
from calendar_bot_db.models.config import settings, storage
from calendar_bot_db.handlers import (strt_end_hdlrs, show_event_detail, show_events_hndl,
                                      register_hdlr, fill_form_hndl, edit_event_hndl,
                                      delete_event_hndl, cancel_hdlrs)


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
    dialog_create_state = Dialog(set_calendar_window)
    dialog_edit_state = Dialog(edit_calendar_window)
    dp.include_router(dialog_create_state)
    dp.include_router(dialog_edit_state)

    # Инициализация DialogManager
    setup_dialogs(dp)

    # Регистрируем роутеры
    dp.include_router(cancel_hdlrs.router)
    dp.include_router(show_events_hndl.router)
    dp.include_router(show_event_detail.router)
    dp.include_router(register_hdlr.router)
    dp.include_router(fill_form_hndl.router)
    dp.include_router(edit_event_hndl.router)
    dp.include_router(delete_event_hndl.router)
    dp.include_router(strt_end_hdlrs.router)

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
