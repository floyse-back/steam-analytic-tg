from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from src.shared.config import steam_commands

async def create_inline_steam_commands():
    steam_inline_keyboard = InlineKeyboardBuilder()

    for v,i in steam_commands.items():
        steam_inline_keyboard.add(
            InlineKeyboardButton(
                text=v,
                callback_data=v
            )
        )

    return steam_inline_keyboard.adjust(2).as_markup()