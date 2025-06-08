from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

user_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Hello World", callback_data="hello_world")],
    ]
)