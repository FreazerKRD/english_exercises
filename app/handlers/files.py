import os
import json
import asyncio
from sentence_splitter import SentenceSplitter
from config import UPLOADED_PATH, EXERCISES_PATH
from aiogram import Router, F, types, Bot

router = Router()

def new_file(file_name: str) -> bool:
    # Sentence splitter
    splitter = SentenceSplitter(language='en')
    
    # Open user file and save into variable
    file_path = os.path.join(UPLOADED_PATH, file_name)
    save_path = os.path.join(EXERCISES_PATH, file_name.replace('txt', 'json'))
    
    with open(file_path, mode="r") as file:
        text = file.read()

    try:
        with open(file_path, mode="r") as file:
            text = file.read()
    except IOError:
        return False

    # Delete uploaded file
    os.remove(file_path)

    # Delete new-line symbols
    text = text.replace('-\n', '').replace('\r', '').replace('\n', ' ')
    
    # Split text on non-null sentences
    sentences = [s for s in splitter.split(text) if s != '']

    # Save splitted text to json
    try:
        with open(save_path, "w") as file:
            json.dump(sentences, file)
            print(f"Done writing JSON data into {save_path}")
            return True
    except:
        return False

@router.message(F.document)
async def download_text(message: types.Message, bot: Bot):
    upload_path = os.path.join(UPLOADED_PATH, message.document.file_name)
    saved_path = os.path.join(EXERCISES_PATH, message.document.file_name.replace('txt', 'json'))
    # Проверка, является ли файл txt, и не был ли загружен ранее
    if message.document.file_name.lower().endswith('.txt') \
            and not os.path.exists(saved_path) \
            and message.document.file_size < 307200:
        await bot.download(
            message.document,
            destination= upload_path)
        result = False
        result = new_file(message.document.file_name)
        if result:
            await message.answer("<i>Книга успешно загружена и сохранена в базе.</i>")
        else:
            await message.answer("<i>Ошибка чтения файла, либо такая книга уже представленна в нашей базе.</i>")
    else:
        await message.answer("<i>Ошибка чтения файла, либо такая книга уже представленна в нашей базе.</i>")