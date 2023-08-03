from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Using list of dicts with books info
def books_kb(posts: list, start_index: int, books_per_page: int) -> InlineKeyboardMarkup | int:

    # Set count of books per page and check if it's out of total books count
    end_index = start_index + books_per_page - 1
    
    builder = InlineKeyboardBuilder()
    
    # Add buttons for books
    for i in range(start_index, end_index): 
        if i == len(posts):
            break
        else:
            # Create button for book and add to keyboard
            builder.add(InlineKeyboardButton(
                text = str(posts[i]['file_name']).replace(".json", ""),
                # Add prefix for filtering is callback query
                callback_data='bs_' + str(posts[i]['id']))
            )
            builder.adjust(1)
    
    # Show only actual buttons
    if start_index <= books_per_page and books_per_page >= len(posts):
        builder.add(InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
        builder.adjust(1)
    
    elif start_index <= books_per_page and end_index < len(posts):
        builder.add(InlineKeyboardButton(text="Вперед", callback_data = "bs_forward"))
        builder.add(InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
        builder.adjust(2)
    
    elif start_index >= books_per_page and end_index >= len(posts):
        builder.add(InlineKeyboardButton(text="Назад", callback_data="bs_back"))
        builder.add(InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
        builder.adjust(2)
    
    else:
        builder.add(InlineKeyboardButton(text="Вперед", callback_data = "bs_forward"))
        builder.add(InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
        builder.add(InlineKeyboardButton(text="Назад", callback_data="bs_back"))
        builder.adjust(3)
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)