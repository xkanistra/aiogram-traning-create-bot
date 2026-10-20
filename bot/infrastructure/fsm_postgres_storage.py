# Хранилище состояний
import json
from typing import Any

from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

from bot.infrastructure.storage_postgres import StoragePostgres


class PostgresFSMStorage(BaseStorage):
    def __init__(self, storage: StoragePostgres) -> None:
        self.storage = storage

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        # Получаем состояние как строку если она есть, иначе принимаем её как пустое значение
        state_str = state.state if state else None

        # Обновляем состояние пользователя, передавая функции telegram_id(key.user_id) и состояние
        await self.storage.update_user_state(key.user_id, state_str)

    async def get_state(self, key: StorageKey) -> str | None:
        # Получаем пользователя из БД
        user = await self.storage.get_user(key.user_id)
        return user.get("state") if user else None

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        # Сохраняем словарь заказа в БД
        await self.storage.update_user_order_json(key.user_id, data)

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        user = await self.storage.get_user(key.user_id)
        if user and user.get("order_json"):
            if isinstance(user["order_json"], str):
                return json.loads(user["order_json"])
            return user["order_json"]
        return {}

    async def close(self) -> None:
        pass
