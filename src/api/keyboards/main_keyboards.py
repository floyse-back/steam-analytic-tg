from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Steam")],
    [KeyboardButton(text="Steam Player"),KeyboardButton(text="Profile")],
    [KeyboardButton(text="Subscribes"),KeyboardButton(text="Help")]
], resize_keyboard=True,input_field_placeholder="Меню"
)

help_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎮 Games",callback_data="games_help"),InlineKeyboardButton(text="🧩 Player",callback_data="player_help")],
    [InlineKeyboardButton(text="👤 User",callback_data="user_help"),InlineKeyboardButton(text="🔔 Subscribe",callback_data="subscribe_help")]
])