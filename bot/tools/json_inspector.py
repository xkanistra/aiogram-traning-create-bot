# Мини утилита для проверки JSON
import json


async def inspect(update):
    print(json.dumps(update, indent=2, ensure_ascii=False))
