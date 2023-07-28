from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Any, Awaitable

class DBMiddleware(BaseMiddleware):
    """
        The middleware makes get db connection from the pool and forwards it to the handler.
    """
    def __init__(self, db) -> None:
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        async with self.db.pool.acquire() as conn:
            async with conn.transaction():
                data['conn'] = conn
                data['pool'] = self.db.pool

                return await handler(event, data)