from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.application.services.user_service import UserService

router = Router(name=__name__)

user_service = UserService()

@router.message(Command("user"))
async def user_help(message: Message):
    await message.delete()
    return await message.answer(user_service.user_help(),parse_mode=ParseMode.MARKDOWN)

#[ ] /wishlist                           — Показати список бажаного
@router.message(Command(commands=["whishlist"]))
async def get_game(message: Message):
    await message.answer("Hello World!")

#[ ] /add_wishlist <game_id>            — Додати гру до wishlist
@router.message(Command(commands=["add_whishlist"]))
async def add_whishlist(message:Message):
    parts = message.text.split()

    await message.answer("Whishlisted game id: {}".format(parts[1]))

#[ ] /delete_game <game_id>             — Видалити гру з wishlist
@router.message(Command(commands=["delete_game_whishlist"]))
async def delete_game(message:Message):
    parts = message.text.split()

    await message.answer("Delete game whishlist {}".format(parts[1]))

# [ ] /my_wishlist_deals                 — Знижки з wishlist
@router.message(Command("my_wishlist_deals"))
async def player_stats(message: Message):
    return await message.reply("Soon...")

#[ ] /user_player <user_id>             — Інфо про іншого користувача
@router.message(Command(commands=["user_steam_id"]))
async def user_player(message:Message):
    parts = message.text.split()

    await message.answer("User player id: {}".format(parts[1]))

#Callback
@router.callback_query(F.data == "user_help")
async def user_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{user_service.user_help()}",parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer()