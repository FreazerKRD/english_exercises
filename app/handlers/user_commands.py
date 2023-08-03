import asyncio
import json
from redis.asyncio import Redis
from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.db_requests import (dump_progress, 
                            get_all_books, 
                            set_book,
                            get_user_information)
from keyboards.book_selection import books_kb

# Инициализация роутера и класса запросов к БД
router = Router()

class select_states(StatesGroup):
    start_idx = State()
    
# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message, **kwargs):
    usr_name = message.from_user.full_name
    await message.answer(f"<b>Приветствую, {usr_name}!</b> \n \n \
Этот бот может помочь тебе в изучении английского языка. \n \n \
Обучение происходит в формате чтения книг на английском языке. Бот генерирует почти в каждом предложении \
задание, например: выбрать правильную форму глагола, правильный вариант предложения и т.д. В меню есть \
команда для настроек пользователя, где ты можешь включить или отключить те или иные виды упражнений. \n \n \
Если желаешь отдохнуть от занятия, рекомендуем использовать команду для сохранения прогресса по книге, \
чтобы точно не начинать потом заново :) \
Помимо чтения книг, которые уже есть в базе бота, ты можешь загрузить свою книгу на английском языке. \
Ограничения: формат книги TXT, \
размер файла не более 300 кбайт. \n \
Для загрузки книги просто отправь её в этот чат.")

# Обработчик команды /select_book
@router.message(Command('select_book'))
async def select_book_command(message: types.Message, 
                              state:FSMContext, 
                              start_index=0, 
                              books_per_page = 5 , 
                              **kwargs):
    data = await state.get_data()
    books_list = await get_all_books(kwargs['conn'])

    await state.set_state(select_states.start_idx)
    # Save current position
    await state.update_data(start_idx = start_index)
    
    await message.answer("Книги в базе данных:", reply_markup=books_kb(books_list, 
                                                                       start_index=start_index, 
                                                                       books_per_page=books_per_page))

@router.callback_query(Text(startswith="bs_"))
async def books_process(callback: types.CallbackQuery, 
                        state:FSMContext,
                        r, 
                        books_per_page=5,
                        **kwargs):
    data = await state.get_data()
    match callback.data.replace("bs_", ""):
        # Add or subtract start
        case "forward":
            _start_idx = data.get("start_idx") + books_per_page
        case "back":
            _start_idx = data.get("start_idx") - books_per_page
        # Exit from book selection
        case "cancel":
            await state.clear()
            await callback.message.delete()
            return
        # Update user's selected book
        case _:
            # Dump progress for previous book to DB
            users_cache = await r.hget(callback.from_user.id, 'cache')
            users_cache = json.loads(users_cache.decode('utf-8'))
            await dump_progress(kwargs['conn'], 
                                user_id=callback.from_user.id, 
                                book_id=users_cache['current_book'],
                                progress=users_cache['current_progress'])
            
            # Get index of new book and save changes to DB
            selected_book_id = int(callback.data.replace("bs_", ""))
            await set_book(kwargs['conn'], callback.from_user.id, selected_book_id)

            # Update user's cache in Redis
            users_cache = await get_user_information(kwargs['conn'], callback.from_user.id)
            cache_str = json.dumps(users_cache, ensure_ascii=False)
            await r.hset(callback.from_user.id, 'cache', cache_str)

            # Exit from book selection
            await callback.answer(text="Книга успешно выбрана!",
                                  show_alert=True)
            await callback.message.delete()
            return
    # Load list of the books
    books_list = await get_all_books(kwargs['conn'])
    # Save new start index
    await state.update_data(start_idx = _start_idx)
    # Edit existing message
    await callback.message.edit_text(text='Книги в базе данных:',
                                     reply_markup=books_kb(books_list, start_index=_start_idx, books_per_page=books_per_page))

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
    
        