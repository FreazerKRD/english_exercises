import os
import json
import aiogram
from config import EXERCISES_PATH
from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from redis.asyncio import Redis
from english_exercises import ExerciseGenerator

# Инициализация роутера и генератора упражнений
router = Router()
eg = ExerciseGenerator()

# Обработчик команды /study
@router.message(Command('study'))
async def study_command(message: types.Message, r):

    # Take user settings and sentences from data of Dispatcher
    users_cache = await r.hget(message.from_user.id, 'cache')
    users_cache = json.loads(users_cache.decode('utf-8'))
    current_book = users_cache['file_name']
    
    # Load book for training
    book_path = os.path.join(EXERCISES_PATH, current_book)
    with open(book_path, 'r') as file:
        users_cache['book_sentences'] = json.load(file)

    cache_str = json.dumps(users_cache, ensure_ascii=False)
    await r.hset(message.from_user.id, 'cache', cache_str)
    
    # Старт работы с упражнениями
    await send_question(message, message.from_user.id, r)

# Отправка вопроса и вариантов ответа
async def send_question(message: types.Message, user_id: int, r: Redis):

    users_cache = await r.hget(user_id, 'cache')
    users_cache = json.loads(users_cache.decode('utf-8'))
    if users_cache['current_progress'] < len(users_cache['book_sentences']):
        exercise = eg.select_exercise(users_cache['book_sentences'][users_cache['current_progress']])
        if exercise:
            users_cache['current_answer'] = exercise['answer']
            sentence = exercise['sentence']
            builder = InlineKeyboardBuilder()
            if exercise['type'] == 'sentence_gen':
                for option in exercise['options']:
                    option_data = 'ex_' + str(option)
                    builder.add(types.InlineKeyboardButton(
                        text = str(option),
                        # Add prefix for filtering is callback query
                        callback_data = option_data)
                    )
                    builder.adjust(1)
                message_text = f"<i>{exercise['description']}</i>"
            else:
                for option in exercise['options']:
                    option_data = 'ex_' + str(option)
                    builder.add(types.InlineKeyboardButton(
                        text = str(option),
                        # Add prefix for filtering is callback query
                        callback_data = option_data)
                    )
                message_text = f"{sentence}{os.linesep}{os.linesep}<i>{exercise['description']}</i>"
            await message.answer(message_text, reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
        else:
            # В случае отстутствия упражнений - вывод текущего предложения и переход к следующему
            await message.answer(f"<b>{users_cache['book_sentences'][users_cache['current_progress']]}</b>")
            users_cache['current_progress'] += 1
            cache_str = json.dumps(users_cache, ensure_ascii=False)
            await r.hset(user_id, 'cache', cache_str)  
            await send_question(message, user_id, r)

        cache_str = json.dumps(users_cache, ensure_ascii=False)
        await r.hset(user_id, 'cache', cache_str)
        
    else:
        await message.answer("Вопросы закончились!")

# Обработчик ответов на вопросы
@router.callback_query(Text(startswith="ex_"))
async def handle_answer(callback: types.CallbackQuery, r: Redis):
    users_cache = await r.hget(callback.from_user.id, 'cache')
    users_cache = json.loads(users_cache.decode('utf-8'))

    user_answer = callback.data.split("_")[1]

    if users_cache['current_progress'] < len(users_cache['book_sentences']):
        if user_answer == users_cache['current_answer']:
            await callback.message.answer("\N{smiling face with sunglasses} Вы выбрали верный ответ: <b>" + 
                                          os.linesep + users_cache['current_answer'] + "</b>")
        else:
            await callback.message.answer("\N{unamused face} Ваш ответ неверный! Правильный: <b>" + os.linesep 
                                          + users_cache['current_answer'] + "</b>")
        users_cache['current_progress'] += 1
        
        cache_str = json.dumps(users_cache, ensure_ascii=False)
        await r.hset(callback.from_user.id, 'cache', cache_str)
        await callback.message.edit_reply_markup()
        await send_question(callback.message, callback.from_user.id, r)

    await callback.answer()