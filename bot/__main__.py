# Основной файл запускающий бота
import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}.{msecs:03.0f}] {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    force=True,
)

logger = logging.getLogger(__name__)

from bot.handlers.message_start import router as start_router
from bot.handlers.pizza_size import router as pizza_size_router
from bot.infrastructure.storage_postgres import StoragePostgres
from bot.middlewares.db_middleware import DatabaseMiddleware


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="[{asctime}.{msecs:03.0f}] {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
        force=True,
    )
    logger = logging.getLogger(__name__)

    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("Переменная окружения BOT_TOKEN не установленна.")

    bot = Bot(token=bot_token)
    dispatcher = Dispatcher()

    logger.info("Инициализация инфраструктуры...")

    storage = StoragePostgres()
    pool = await storage._get_pool()

    dispatcher.update.middleware(DatabaseMiddleware(storage))
    dispatcher.include_router(start_router)
    dispatcher.include_router(pizza_size_router)
    logger.info("Бот успешно запущен и готов к работе.")

    try:
        await dispatcher.start_polling(bot)
    finally:
        await pool.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
