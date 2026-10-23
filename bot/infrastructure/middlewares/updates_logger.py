import logging
from collections.abc import Awaitable, Callable
from os import getenv
from typing import Any

import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import Update
from dotenv import load_dotenv

from bot.infrastructure.storage_postgres import StoragePostgres

load_dotenv()

# Проверка запущен ли тест, для того чтобы не спамить тестовыми запросами в БД
IS_TESTING = getenv("TESTING", "FALSE") in ("true", "1", "yes")

logger = logging.getLogger(__name__)


# Middleware для автоматической записи всех входящих апдейтов Telegram в БД
class UpdateLoggerMiddleware(BaseMiddleware):
    def __init__(self, storage: StoragePostgres):
        self.storage = storage
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        # Если вкл тестирование пропускаем логгирование в базу
        if not IS_TESTING:
            try:
                # model_dump преобразует Pydantic-модель aiogram в чистый dict
                update_dict = event.model_dump(exclude_none=True)
                await self.storage.persist_updates([update_dict])
            except asyncpg.PostgresError as e:
                # Если запись не удалась, мы обязательно увидим ошибку в консоли докера!
                logger.error(
                    f"[MIDDLEWARE ERROR] Не удалось сохранить апдейт в БД: {e}"
                )

        return await handler(event, data)
