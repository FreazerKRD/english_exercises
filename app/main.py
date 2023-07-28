import asyncio
import logging
import config
from aiogram import Bot, Dispatcher
from handlers import questions, files
from db.db_middleware import DBMiddleware
from db.db_connection import create_connection

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Запуск бота
async def main():
    # Инициализация бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Подключение к PostgreSQL
    db = create_connection()
    await db.on_startup()

    # Регистрация роутеров
    dp.include_routers(questions.router, files.router)

    # Подключение миддлваря с пулом PostgreSQL
    dp.update.outer_middleware(DBMiddleware(db))

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())