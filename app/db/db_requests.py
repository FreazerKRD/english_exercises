import asyncio

# Add user to DB
async def user_registration(conn, user_id: int) -> int | None:
    row = await conn.fetchrow('SELECT * FROM users WHERE telegram_id = $1', user_id)
    if row:
        print(f'User id {user_id} already in DB.')
        return row.get('telegram_id')
    else:
        if await conn.execute('INSERT INTO users (telegram_id) \
                                VALUES ($1) \
                                ON CONFLICT (telegram_id) DO NOTHING;', 
                                user_id):
            print(f'User added, id: {user_id}')
            return user_id
        else:
            print('Error adding new user!')
            return None
        
# Get user information and return to save in cache
async def get_user_information(conn, user_id: int) -> dict:
    row = await conn.fetchrow('SELECT * FROM users WHERE telegram_id = $1', user_id)
    if row:
        row = dict(row)
        progress = await conn.fetchrow('SELECT * FROM user_books WHERE user_id = $1 AND book_id = $2', 
                                       row['telegram_id'], row['current_book'])
        if progress:
            row['current_progress'] = dict(progress)['progress']
            return row
        else:
            await conn.execute('INSERT INTO user_books (user_id, book_id) \
                                VALUES ($1, $2);', 
                                row['telegram_id'], row['current_book'])
            row['current_progress'] = 0
            return row

# Add information about new file to DB        
async def add_file(conn, file_name: str) -> int | None:
    row = await conn.fetchrow('SELECT * FROM books WHERE file_name = $1', file_name)
    if row:
        print(f'Book {file_name} already in DB.')
        return row.get('id')
    else:
        if await conn.execute('INSERT INTO books (file_name) \
                                VALUES ($1) \
                                ON CONFLICT (file_name) DO NOTHING;', 
                                file_name):
            print(f'Book added {file_name}')
            row = await conn.fetchrow('SELECT * FROM books WHERE file_name = $1', file_name)
            return row.get('id')
        else:
            print('Error adding new book!')
            return None
        
# Set book for exercises
async def set_book(conn, user_id: int, book_id: int) -> None:
    if await conn.fetchrow('SELECT 1 FROM users WHERE "telegram_id" = $1', user_id):
        await conn.execute('UPDATE users \
            SET "current_book" = $1 \
            WHERE "telegram_id" = $2;', 
            book_id, user_id)

# Set user types of exercises
async def set_exercises(conn, user_id: int, exercise_adjective_form: bool, 
                        exercise_verb_form: bool, exercise_sentence_gen: bool) -> None:
    if await conn.fetchrow('SELECT 1 FROM users WHERE "telegram_id" = $1', user_id):
        await conn.execute('UPDATE users \
                           SET "exercise_adjective_form" = $2, \
                           "exercise_verb_form" = $3, \
                           "exercise_sentence_gen" = $4 \
                           WHERE "telegram_id" = $1;', 
                           user_id, exercise_adjective_form, exercise_verb_form, exercise_sentence_gen)