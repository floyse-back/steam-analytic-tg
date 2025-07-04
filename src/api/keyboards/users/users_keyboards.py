from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.shared.config import user_commands

async def create_user_inline_keyboard():
    user_inline_keyboard = InlineKeyboardBuilder()

    for v,i in user_commands.items():
        user_inline_keyboard.add(InlineKeyboardButton(text=v, callback_data=i))

    return user_inline_keyboard.adjust(2).as_markup()

wishlist_inline_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Додати гру до списку бажаного", callback_data="add_wishlist_game"),
            InlineKeyboardButton(text="🗑️ Видалити гру зі списку", callback_data="delete_wishlist_game")
        ],
        [
            InlineKeyboardButton(text="👤 Перейти до профілю", callback_data="user_main")
        ]
    ]
)

back_to_profile_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Назад до меню", callback_data="user_main")
        ]
    ]
)

profile_cancel_inline_keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⏰ Нагадати пізніше", callback_data="profile_cancel_state")
        ]
    ]
)
