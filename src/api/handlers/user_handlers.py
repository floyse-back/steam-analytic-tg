from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command

from src.api.keyboards.users.users_keyboards import create_user_inline_keyboard
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.shared.config import MainMenu, user_message_menu

router = Router(name=__name__)

user_service = UsersService(
    users_repository=UsersRepository(),
)


@router.message(Command("user"))
async def user_help(message: Message):
    await message.delete()
    return await message.answer(user_service.user_help(),parse_mode=ParseMode.MARKDOWN)

@router.message(lambda message: message.text == f"{MainMenu.profile}")
async def user_reply(message: Message):
    await message.delete()
    await message.answer(text=f"{user_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_user_inline_keyboard())

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
@router.message(Command("my_whishlist_deals"))
async def player_stats(message: Message):
    return await message.reply("Soon...")

#[ ] /user_player <user_id>             — Інфо про іншого користувача
@router.message(Command(commands=["user_steam_id"]))
async def user_player(message:Message):
    parts = message.text.split()

    await message.answer("User player id: {}".format(parts[1]))