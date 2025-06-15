from aiogram.utils.keyboard import InlineKeyboardButton,InlineKeyboardMarkup, InlineKeyboardBuilder
from src.shared.config import steam_commands

async def create_inline_steam_commands():
    steam_inline_keyboard = InlineKeyboardBuilder()

    for v,i in steam_commands.items():
        steam_inline_keyboard.add(
            InlineKeyboardButton(
                text=v,
                callback_data=i
            )
        )

    return steam_inline_keyboard.adjust(2).as_markup()

search_new_game_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎮🔄 — Знайти іншу гру",callback_data="search_game")]
    ]
)

async def create_player_details_inline(callback_data,text):
    inline_buttons = InlineKeyboardBuilder()
    inline_buttons.add(
        InlineKeyboardButton(
            text=f"{text}",
            callback_data=callback_data
        )
    )
    return inline_buttons.adjust(1).as_markup()
