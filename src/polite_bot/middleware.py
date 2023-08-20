from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from src.polite_bot.services import Repository


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, pool: ConnectionPool):
        self._pool = pool

    async def __call__(
            self, handler: Callable[[types.Message or types.CallbackQuery,
                                     Dict[str, Any]], Awaitable[Any]],
            event: types.Message or types.CallbackQuery, data: Dict[str, Any]
    ) -> Any:
        redis: Redis = await Redis(connection_pool=self._pool)
        try:
            data['repo'] = Repository(redis)
            await handler(event, data)
        finally:
            await redis.close()
        del data['repo']
