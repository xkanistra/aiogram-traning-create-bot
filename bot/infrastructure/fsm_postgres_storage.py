# Хранилище состояний
import json
from typing import Any

from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

from bot.infrastructure.storage_postgres import StoragePostgres


class PostgresFSMStorage(BaseStorage):
    def __init__(self, storage: StoragePostgres) -> None:
        self.storage = storage

    async def get_state(self, key: StorageKey) -> str | None:
        await self.storage.ensure_users_exists(key.user_id)

        # Получаем пользователя из БД
        user = await self.storage.get_user(key.user_id)
        state_from_db = user.get("state") if user else None
        print(
            f"🔍 [FSM ЧТЕНИЕ] Юзер {key.user_id} -> Из БД пришло: {state_from_db}"
        )  # ДОБАВИТЬ ПРИНТ
        return state_from_db

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        state_str = state.state if state else None
        # Гарантируем наличие пользователя перед любым UPDATE
        await self.storage.ensure_users_exists(key.user_id)

        print(
            f"📡 [FSM ЗАПИСЬ СТЕЙТА] Юзер {key.user_id} -> Устанавливаем: {state_str}"
        )

        # Вызываем ваш метод обновления стейта
        await self.storage.update_user_state(key.user_id, state_str)

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        # Гарантируем наличие пользователя перед сохранением словаря заказа
        await self.storage.ensure_users_exists(key.user_id)
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
