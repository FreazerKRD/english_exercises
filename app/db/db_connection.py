import asyncpg
import logging
from config import DB_HOST, DB_NAME, DB_USER, DB_PASS

logger = logging.getLogger(__name__)


class DataBase:
    def __init__(self, host: str, name: str, user: str, password: str):
        self._pool = None
        self.host = host
        self.name = name
        self.user = user
        self.password = password
    
    @property
    def pool(self) -> asyncpg.Pool:
        if isinstance(self._pool, asyncpg.Pool):
            return self._pool
        else:
            raise ValueError(
                'Pool is not initialized. You should call on_startup function first.')

    async def on_startup(self):
        self._pool = await asyncpg.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.name
        )

    async def on_shutdown(self):
        await self.pool.close()


def create_connection(host=DB_HOST, name=DB_NAME, user=DB_USER, password=DB_PASS):
    return DataBase(host, name, user, password)


db = create_connection()