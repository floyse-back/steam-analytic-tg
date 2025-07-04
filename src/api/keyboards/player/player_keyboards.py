from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.shared.config import player_commands


async def create_inline_player_commands():
    player_inline_keyboard = InlineKeyboardBuilder()

    for v,i in player_commands.items():
        player_inline_keyboard.add(
            InlineKeyboardButton(
                text=v,
                callback_data=i
            )
        )

    return player_inline_keyboard.adjust(2).as_markup()

back_to_menu_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text= "Повернутися до меню 🔙",callback_data="player_menu")]
    ]
)
back_to_menu_inline_callback_close_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text= "Повернутися до меню 🔙",callback_data="player_menu_callback_close")]
    ]
)

def find_other_player(callback_data:str):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="Знайти іншого користувача 🔍",callback_data=callback_data)],
            [InlineKeyboardButton(text="Повернутися до меню 🔙",callback_data="player_menu_callback_close")]
        ]
    )
    return inline_keyboard