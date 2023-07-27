import time
import asyncio
import logging
from socket import gaierror
from db_connection import create_connection

logger = logging.getLogger('wait_for_db')

db = create_connection()

async def main():
    num_retries = 60
    wait_time = 1

    print("\033[32mWait for DB was ready.")
    for _ in range(num_retries):
        try:
            await db.on_startup()
            try:
                async with db.pool.acquire() as conn:
                    await conn.execute('SELECT 1')
                print(f"\n\033[32mDB is ready!\033[0m")
                break
            finally:
                await db.on_shutdown()
        except (gaierror, ConnectionRefusedError):
            print(".", end="", flush=True)
            time.sleep(wait_time)
    else:
        print(f"\n\033[31mCouldn't connect to database after {num_retries} attempts, exiting...\033[0m")
        exit(1)

if __name__ == '__main__':
    asyncio.run(main())