import asyncio
from aiogram import Router, types
from aiogram.filters import Command

# Инициализация роутера и класса запросов к БД
router = Router()

# def register_user(message):
#     user_id = message.from_user.id if message.from_user.id else None
#     username = message.from_user.username if message.from_user.username else None
#     user = User(id=int(message.from_user.id), username=username, name=message.from_user.full_name)

#     session.add(user)

#     try:
#         session.commit()
#         return True
#     except IntegrityError:
#         session.rollback()  # откатываем session.add(user)
#         return False
    
# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message, **kwargs):
    await message.answer("Добро пожаловать!")
    
    # await conn.execute('INSERT INTO books (file_name) VALUES ($1) ON CONFLICT (file_name) DO NOTHING;', 
    #                            message.document.file_name.replace('txt', 'json'))
    # ##### ЗДЕСЬ НУЖНО БУДЕТ БРАТЬ ПРОГРЕСС ИЗ БД! #####
    # global current_question_index
    # global book_sentences
    # current_question_index = 0
    # # Загружаем книгу для упражнений
    # book_path = os.path.join(EXERCISES_PATH, current_book)
    # with open(book_path, 'r') as file:
    #     book_sentences = json.load(file)
    # # Старт работы с упражнениями
    # await send_question(message)