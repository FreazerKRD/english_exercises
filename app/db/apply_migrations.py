import asyncpg
import asyncio
import glob
from db.db_connection import create_connection
import logging


logger = logging.getLogger('apply_migrations')


async def apply_migrations(conn: asyncpg.Connection):
    await conn.execute('CREATE TABLE IF NOT EXISTS schema_version (version int);')
    current_version = await conn.fetchval('SELECT version FROM schema_version;')
    if current_version is None:
        current_version = 0
        await conn.execute('INSERT INTO schema_version (version) VALUES ($1);', current_version)
    migration_files = sorted(glob.glob('db/migrations/*.sql'), key=lambda x: int(x.split('/')[-1].split('_')[0]))
    migrations_applied = 0
    for filename in migration_files:
        # extract version from filename
        version = int(filename.split('/')[-1].split('_')[0])
        if version > current_version:
            logger.info(f'Applying migration {filename}')
            with open(filename, 'r') as f:
                await conn.execute(f.read())
            await conn.execute('UPDATE schema_version SET version = $1;', version)
            migrations_applied += 1
    if migrations_applied > 0:
        logger.info(f'Applied {migrations_applied} migrations.')
    else:
        logger.info('No migrations for applying.')
    


async def main():
    db = create_connection()
    await db.on_startup()
    async with db.pool.acquire() as conn:
        await apply_migrations(conn)
    await db.on_shutdown()

if __name__ == '__main__':
    asyncio.run(main())
