# Основной файл запускающий бота
import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}.{msecs:03.0f}] {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{",
    force=True,
)

logger = logging.getLogger(__name__)


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

    # TODO. Дальше тут подключится StoragePostgres
    # и DatabaseMiddleware

    logger.info("Бот успешно запущен и готов к работе.")

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен.")
