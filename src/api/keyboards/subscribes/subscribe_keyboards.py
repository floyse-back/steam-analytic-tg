from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.shared.config import subscribes_commands


async def create_inline_subscribes_commands():
    subscribes_inline_keyboard = InlineKeyboardBuilder()

    for v,i in subscribes_commands.items():
        subscribes_inline_keyboard.add(
            InlineKeyboardButton(
                text=v,
                callback_data=i
            )
        )

    return subscribes_inline_keyboard.adjust(2).as_markup()