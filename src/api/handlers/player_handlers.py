from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from src.application.services.player_service import PlayerService

router = Router(name=__name__)

player_service = PlayerService()

@router.message(Command("player"))
async def player_help(message: Message):
    await message.delete()
    return await message.answer(player_service.player_help(),parse_mode=ParseMode.MARKDOWN)

# [ ] /user_full_stats <user_id>         — Повна статистика
@router.message(Command("user_full_stats"))
async def user_full_stats(message: Message):
    return await message.reply("Soon...")

# [ ] /user_rating <user_id>             — Рейтинг
@router.message(Command("user_rating"))
async def player_rating(message: Message):
    return await message.reply("Soon...")

# [ ] /achievements_user <user_id>       — Досягнення
@router.message(Command("achievements_player"))
async def achievements_player(message: Message):
    return await message.reply("Soon...")

# [ ] /user_stalkering <user_id>         — Відстеження профілю
@router.message(Command("player_stalkering"))
async def player_stalkering(message: Message):
    return await message.reply("Soon...")

# [ ] /player_play                         — Виявлення активної гри
@router.message(Command("player_play"))
async def player_play(message: Message):
    return await message.reply("Soon...")
# [ ] /compare_users <user1> <user2>     — Порівняння користувачів
@router.message(Command("compare_users"))
async def compare_users(message: Message):
    return await message.reply("Soon...")
# [ ] /friend_activity                   — Активність друзів (опціонально)
@router.message(Command("friend_activity"))
async def compare_players(message: Message):
    return await message.reply("Soon...")

#Callback
@router.callback_query(F.data == "player_help")
async def player_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{player_service.player_help()}",parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer()