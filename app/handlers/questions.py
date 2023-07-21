import os
import pandas as pd
import aiogram
import emoji
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
current_book = 'Little_Red_Cap_ Jacob_and_Wilhelm_Grimm.txt'
df = pd.DataFrame()

# Обработчик команды /start
@router.message(Command('start'))
async def start_command(message: types.Message):
    ##### ЗДЕСЬ НУЖНО БУДЕТ БРАТЬ ПРОГРЕСС ИЗ БД! #####
    global current_question_index
    global df
    current_question_index = 0
    # Загружаем книгу для упражнений
    book_path = os.path.join(EXERCISES_PATH, current_book)
    df = pd.read_csv(book_path)
    df = df.loc[:10,:]
    # Старт работы с упражнениями
    await send_question(message)

# Отправка вопроса и вариантов ответа
async def send_question(message: types.Message):
    global current_question_index
    global current_answer
    
    if current_question_index < len(df):
        exercise = eg.exercise_adjective_form(df.loc[current_question_index,'raw'])
        if exercise:
            current_answer = exercise['answer']
            sentence = exercise['sentence']
            builder = InlineKeyboardBuilder()
            for option in exercise['options']:
                builder.add(types.InlineKeyboardButton(
                    text=str(option),
                    callback_data=str(option))
                )
            await message.answer(sentence, reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True))
        else:
            # В случае отстутствия упражнений - вывод текущего предложения и переход к следующему
            await message.answer(df.loc[current_question_index,'raw'])
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
    if current_question_index < len(df):
        if user_answer == current_answer:
            await callback.message.answer(emoji.emojize(":partying_face:") + " Вы выбрали верный ответ!")
        else:
            await callback.message.answer(emoji.emojize(":sneezing_face:") + " Ваш ответ не верный! Правильный: " + current_answer)
        current_question_index += 1
        await send_question(callback.message)

    await callback.answer()