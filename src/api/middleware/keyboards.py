from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_subscribe = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text="Перевірити підписку",
            callback_data="check_subscribe"
        )]
    ]
)