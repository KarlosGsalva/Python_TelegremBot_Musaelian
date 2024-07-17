import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from calendar_bot_db.models.config import settings, storage
from calendar_bot_db.handlers import get_routers


from colorlog import ColoredFormatter

from calendar_bot_db.services import set_main_menu_cmds

import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ------ настройка логов ---------

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

color_formatter = ColoredFormatter(
    "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    reset=True,
    log_colors={
        "DEBUG": "yellow",
        "INFO": "green",
        "WARNING": "cyan",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
    secondary_log_colors={},
)

for handler in logging.root.handlers:
    handler.setFormatter(color_formatter)

logger = logging.getLogger(__name__)

# ---------------

BOT_TOKEN = settings.bot_token.get_secret_value()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


@dp.startup()
async def on_startup() -> None:
    # Регистрируем роутеры
    dp.include_routers(*get_routers(dp))

    # Установка команд основного меню бота
    await set_main_menu_cmds(bot=bot)


async def main():
    logger.debug(f"{10 * '-'} START {10 * '-'}")
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.debug(f"{10 * '-'} KeyboardInterrupt {10 * '-'}")
        exit()
