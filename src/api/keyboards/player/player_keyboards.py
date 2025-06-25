from aiogram.types import InlineKeyboardButton
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