import os
from dotenv import load_dotenv

def get_env_value(name: str) -> str:
    value = os.getenv(name, None)
    if value is None:
        raise ValueError(
            f'{name} environment variable should be filled in the OS.')
    return value

# Loading .env if run without Docker
BOT_TOKEN = os.getenv('BOT_TOKEN', None)
if BOT_TOKEN is None:
    load_dotenv()

# Bot API token
BOT_TOKEN = get_env_value('BOT_TOKEN')
# Root path of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to texts with exercises and uploaded texts
EXERCISES_PATH = os.path.join(ROOT_DIR, 'exercises_texts/')
UPLOADED_PATH = os.path.join(ROOT_DIR,'uploaded_texts/')