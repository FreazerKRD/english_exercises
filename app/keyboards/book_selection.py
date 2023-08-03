from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Using list of dicts with books info
def books_kb(posts: list, start_index: int, books_per_page: int) -> InlineKeyboardMarkup | int:

    # Set count of books per page and check if it's out of total books count
    end_index = start_index + books_per_page
    
    builder = InlineKeyboardBuilder()
    
    # Add buttons for books
    for i in range(start_index, end_index): 
        if i == len(posts):
            break
        else:
            # Create button for book and add to keyboard
            builder.row(InlineKeyboardButton(
                text = str(posts[i]['file_name']).replace(".json", ""),
                # Add prefix for filtering is callback query
                callback_data='bs_' + str(posts[i]['id']))
            )
    
    # Show only actual buttons
    if start_index < books_per_page and books_per_page >= len(posts):
        builder.row(InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
    
    elif start_index < books_per_page and end_index < len(posts):
        builder.row(InlineKeyboardButton(text="Вперед", callback_data = "bs_forward"), 
                    InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
    
    elif start_index >= books_per_page and end_index >= len(posts):
        builder.row(InlineKeyboardButton(text="Назад", callback_data="bs_back"), 
                    InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"))
    
    else:
        builder.row(InlineKeyboardButton(text="Вперед", callback_data = "bs_forward"), 
                    InlineKeyboardButton(text="Отмена", callback_data="bs_cancel"), 
                    InlineKeyboardButton(text="Назад", callback_data="bs_back"))
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)