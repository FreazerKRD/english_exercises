import os
import json
import aiogram
from config import EXERCISES_PATH
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from english_exercises import ExerciseGenerator

# Инициализация роутера и генератора упражнений
router = Router()
eg = ExerciseGenerator()

# Глобальные переменные
current_question_index = 0
current_answer = ''
current_book = 'Little_Red_Cap_ Jacob_and_Wilhelm_Grimm.json'
book_sentences = []

# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message):
    ##### ЗДЕСЬ НУЖНО БУДЕТ БРАТЬ ПРОГРЕСС ИЗ БД! #####
    global current_question_index
    global book_sentences
    current_question_index = 0
    # Загружаем книгу для упражнений
    book_path = os.path.join(EXERCISES_PATH, current_book)
    with open(book_path, 'r') as file:
        book_sentences = json.load(file)
    # Старт работы с упражнениями
    await send_question(message)

# Отправка вопроса и вариантов ответа
async def send_question(message: types.Message):
    global current_question_index
    global current_answer
    
    if current_question_index < len(book_sentences):
        exercise = eg.select_exercise(book_sentences[current_question_index])
        if exercise:
            current_answer = exercise['answer']
            sentence = exercise['sentence']
            builder = InlineKeyboardBuilder()
            if exercise['type'] == 'sentence_gen':
                for option in exercise['options']:
                    builder.add(types.InlineKeyboardButton(
                        text=str(option),
                        callback_data=str(option))
                    )
                    builder.adjust(1)
                message_text = f"<i>{exercise['description']}</i>"
            else:
                for option in exercise['options']:
                    builder.add(types.InlineKeyboardButton(
                        text=str(option),
                        callback_data=str(option))
                    )
                message_text = f"{sentence}{os.linesep}{os.linesep}<i>{exercise['description']}</i>"
            await message.answer(message_text, reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
        else:
            # В случае отстутствия упражнений - вывод текущего предложения и переход к следующему
            await message.answer(f"<b>{book_sentences[current_question_index]}</b>")
            current_question_index += 1
            await send_question(message)
    else:
        await message.answer("Вопросы закончились!")

# Обработчик ответов на вопросы
@router.callback_query()
async def handle_answer(callback: types.CallbackQuery):
    global current_question_index
    global current_answer
    user_answer = callback.data
    if current_question_index < len(book_sentences):
        if user_answer == current_answer:
            await callback.message.answer("\N{smiling face with sunglasses} Вы выбрали верный ответ!")
        else:
            await callback.message.answer("\N{unamused face} Ваш ответ не верный! Правильный: <b>" + current_answer + "</b>")
        current_question_index += 1
        await send_question(callback.message)

    await callback.answer()