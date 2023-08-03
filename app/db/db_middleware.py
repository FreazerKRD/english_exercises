from aiogram import BaseMiddleware
from aiogram.types import Update
from redis.asyncio import Redis
from typing import Callable, Any, Awaitable
from db.db_requests import user_registration, get_user_information
import json

class DBMiddleware(BaseMiddleware):
    """
        The middleware makes get db connection from the pool and forwards it to the handler.
    """
    def __init__(self, db, r: Redis) -> None:
        self.db = db
        self.r = r
        self.cache = {}

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        # Initialization of pool connections for all handlers 
        # and save to the kwargs of Dispatcher(data)
        data['r'] = self.r

        async with self.db.pool.acquire() as conn:
            async with conn.transaction():
                data['conn'] = conn
                data['pool'] = self.db.pool

                # Extract user_id from any type of events
                event_object = getattr(event, event.event_type)
                user_id = event_object.from_user.id

                # Register user and save it's information into cache
                if user_id != None:

                    uc = await self.r.hget(user_id, 'cache')
                    if not uc:
                        await user_registration(conn=conn, user_id=user_id)
                        user_cache = await get_user_information(conn, user_id)
                        cache_str = json.dumps(user_cache, ensure_ascii=False)
                        await self.r.hset(user_id, 'cache', cache_str)

                return await handler(event, data)