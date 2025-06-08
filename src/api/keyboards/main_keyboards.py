from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from src.shared.config import MainMenu

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"{MainMenu.steam}")],
    [KeyboardButton(text=f"{MainMenu.player}"),KeyboardButton(text=F"{MainMenu.profile}")],
    [KeyboardButton(text=f"{MainMenu.subscribes}"),KeyboardButton(text=f"{MainMenu.help}")],
], resize_keyboard=True,input_field_placeholder=f"{MainMenu.subtitle}"
)

help_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎮 Games",callback_data="games_help"),InlineKeyboardButton(text="🧩 Player",callback_data="player_help")],
    [InlineKeyboardButton(text="👤 User",callback_data="user_help"),InlineKeyboardButton(text="🔔 Subscribe",callback_data="subscribe_help")]
])

back_help_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад",callback_data="help_back")]
])