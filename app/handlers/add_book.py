import os
import pandas as pd
from sentence_splitter import SentenceSplitter
from app.config import UPLOADED_PATH, EXERCISES_PATH
from aiogram import Router, F, types, Bot

router = Router()

def new_file(file_name: str) -> pd.DataFrame:
    # Sentence splitter
    splitter = SentenceSplitter(language='en')
    
    # Open user file and save into variable
    file_path = os.path.join(UPLOADED_PATH, file_name)
    save_path = os.path.join(EXERCISES_PATH, file_name)
    
    with open(file_path, mode="r") as file:
        text = file.read()

    # Delete uploaded file
    os.remove(file_path)

    # Delete new-line symbols
    text = text.replace('-\n', '').replace('\r', '').replace('\n', ' ')
    
    # Split text on non-null sentences and save in DF
    sentences = splitter.split(text=text)
    sentences = [x for x in sentences if x != '']
    df = pd.DataFrame(sentences, columns=['raw'])

    # Save splitted text to csv
    df.to_csv(save_path, index=False)

@router.message(F.document)
async def download_text(message: types.Message, bot: Bot):
    upload_path = os.path.join(UPLOADED_PATH, message.document.file_name)
    saved_path = os.path.join(EXERCISES_PATH, message.document.file_name)
    # Проверка, является ли файл txt, и не был ли загружен ранее
    if message.document.file_name.lower().endswith('.txt') and not os.path.exists(saved_path):
        await bot.download(
            message.document,
            destination= upload_path)
        new_file(message.document.file_name)
        