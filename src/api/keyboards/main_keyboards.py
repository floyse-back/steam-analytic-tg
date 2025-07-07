from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from src.shared.config import MainMenu

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"{MainMenu.steam}")],
    [KeyboardButton(text=f"{MainMenu.player}"),KeyboardButton(text=F"{MainMenu.profile}")],
    [KeyboardButton(text=f"{MainMenu.subscribes}")],
], resize_keyboard=True,input_field_placeholder=f"{MainMenu.subtitle}"
)
