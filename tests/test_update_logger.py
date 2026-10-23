from unittest.mock import AsyncMock, MagicMock

from aiogram.types import Update

from bot.infrastructure.middlewares.updates_logger import UpdateLoggerMiddleware
from bot.infrastructure.storage_postgres import StoragePostgres


async def test_update_logger_middleware_calls_persist_updates() -> None:
    # Настройка Мок репозитория БД
    mock_storage = MagicMock(spec=StoragePostgres)
    mock_storage.persist_updates = AsyncMock()

    middleware = UpdateLoggerMiddleware(storage=mock_storage)

    # Имитация входящего апдейта от ТГ
    mock_update = MagicMock(spec=Update)
    mock_update.model_dump.return_value = {"update_id": 12345}

    # Мокаем следующий хендлер в цепочке aiogram
    mock_handler = AsyncMock(return_value="handler_response")
    mock_data: dict = {}

    # Запуск middleware
    result = await middleware(handler=mock_handler, event=mock_update, data=mock_data)

    # Проверяем что управление передалось дальше и метод вызвался
    assert result == "handler_response"
    mock_handler.assert_called_once_with(mock_update, mock_data)
    mock_storage.persist_updates.assert_called_once_with([{"update_id": 12345}])
