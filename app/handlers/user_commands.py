import asyncio
from aiogram import Router, types
from aiogram.filters import Command

# Инициализация роутера и класса запросов к БД
router = Router()
    
# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message, **kwargs):
    await message.answer("Добро пожаловать!")