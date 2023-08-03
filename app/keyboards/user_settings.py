from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def user_settings_kb() -> InlineKeyboardMarkup:
    
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Включить", callback_data="us_on"),
                InlineKeyboardButton(text="Отключить", callback_data="us_off"))
    
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)