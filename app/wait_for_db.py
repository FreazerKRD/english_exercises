import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from db.database import DATABASE_URL

db_url = DATABASE_URL

engine = create_engine(db_url)

num_retries = 60
wait_time = 1

print("\033[32mWait for DB was ready.")
for i in range(num_retries):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"\n\033[32mDB is ready!\033[0m")
            break
    except OperationalError:
        print(".", end="", flush=True)
        time.sleep(wait_time)
else:
    print(f"\n\033[31mCouldn't connect to database after {num_retries} attempts, exiting...\033[0m")
    exit(1)