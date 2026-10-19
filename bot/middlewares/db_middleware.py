from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.infrastructure.storage_postgres import StoragePostgres


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, storage: StoragePostgres) -> None:
        super().__init__()
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        # Вытаскиваем автоматически id пользователя из любого типа события
        telegram_id = None
        if isinstance(event, Message) and event.from_user or isinstance(event, CallbackQuery) and event.from_user:
            telegram_id = event.from_user.id

        # Если id получено, то гарантом добавляем пользователя в БД
        if telegram_id:
            await self.storage.ensure_users_exists(telegram_id)

        # Пробрасываем хранилище БД в хендлеры
        data["storage"] = self.storage
        # Передача управления след. хендлеру
        return await handler(event, data)
