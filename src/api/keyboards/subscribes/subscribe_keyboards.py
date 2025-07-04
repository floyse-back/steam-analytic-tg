from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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

def create_subscribes_keyboard(callback_data: str, user_id: str):
    inline_keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Підписатися", callback_data=f"subscribe:{callback_data}:{user_id}"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="subscribe_main")
            ],
        ]
    )
    return inline_keyboard_markup

def create_unsubscribes_keyboard(callback_data: str, user_id: str):
    inline_keyboard_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚫 Відписатися", callback_data=f"unsubscribe:{callback_data}:{user_id}"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="subscribe_main")
            ]
        ]
    )
    return inline_keyboard_markup

inline_back_subscribe_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад до підписок", callback_data="subscribe_main")]
    ]
)