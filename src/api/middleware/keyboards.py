from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

check_subscribe = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
            text="Перевірити підписку",
            callback_data="check_subscribe"
        )]
    ]
)
start_command_use = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(
            text="/start"
        )
    ]]
)