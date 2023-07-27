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

BOT_TOKEN = get_env_value('BOT_TOKEN')
DB_HOST = os.getenv('DB_HOST', None)
DB_NAME = os.getenv('DB_NAME', None)
DB_USER = os.getenv('DB_USER', None)
DB_PASS = os.getenv('DB_PASS', None)

# Root path of the project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to texts with exercises and uploaded texts
EXERCISES_PATH = os.path.join(ROOT_DIR, 'exercises_texts/')
UPLOADED_PATH = os.path.join(ROOT_DIR,'uploaded_texts/')
# Path to database
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}" 