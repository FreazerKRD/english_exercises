from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Any, Awaitable
from db.db_requests import user_registration, get_user_information

class DBMiddleware(BaseMiddleware):
    """
        The middleware makes get db connection from the pool and forwards it to the handler.
    """
    def __init__(self, db) -> None:
        self.db = db
        self.cache = {}

    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        # Initialization of pool connections for all handlers 
        # and save to the kwargs of Dispatcher(data)
        async with self.db.pool.acquire() as conn:
            async with conn.transaction():
                data['conn'] = conn
                data['pool'] = self.db.pool
                data['users_cache'] = self.cache

            # Extract user_id from any type of events
            event_object = getattr(event, event.event_type)
            user_id = event_object.from_user.id

            # Register user and save it's information into cache
            if user_id != None:
                user_cache = {}

                user_reg_res = await user_registration(conn=conn, user_id=user_id)
                if user_reg_res:
                    user_cache = await get_user_information(conn=conn, user_id=user_reg_res)
                    self.cache[user_reg_res] = user_cache

            return await handler(event, data)