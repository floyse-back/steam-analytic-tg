from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.shared.config import user_commands

user_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Hello World", callback_data="hello_world")],
    ]
)


async def create_user_inline_keyboard():
    user_inline_keyboard = InlineKeyboardBuilder()

    for v,i in user_commands.items():
        user_inline_keyboard.add(InlineKeyboardButton(text=v, callback_data=i))

    return user_inline_keyboard.adjust(2).as_markup()

wishlist_inline_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Додати гру",callback_data="add_wishlist_game"),InlineKeyboardButton(text="Видалити гру",callback_data="delete_wishlist_game")],
        [InlineKeyboardButton(text="Профіль",callback_data="user_main")]
    ]
)