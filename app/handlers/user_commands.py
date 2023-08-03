import asyncio
from aiogram import Router, types
from aiogram.filters import Command

# Инициализация роутера и класса запросов к БД
router = Router()
    
# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message, **kwargs):
    await message.answer("Добро пожаловать!")

# Обработчик команды /stop_train
@router.message(Command('stop_train'))
async def stop_train_command(message: types.Message, r, **kwargs):
    users_cache = await r.hget(message.from_user.id, 'cache')
    users_cache = json.loads(users_cache.decode('utf-8'))

    user_id = message.from_user.id
    book_id = users_cache['current_book']
    progress = users_cache['current_progress']

    conn = kwargs['conn']
    await dump_progress(conn, user_id, book_id, progress)
    
        