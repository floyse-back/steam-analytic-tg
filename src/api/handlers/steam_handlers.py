from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)

# [ ] /search_game <назва>                — Пошук гри
@router.message(Command("search_game"))
async def search_game(message: Message):
    return await message.reply("Soon...")

#[ ] /free_games_now                     — Актуальні безкоштовні ігри (Steam + Epic)
@router.message(Command("free_games_now"))
async def free_games_now(message: Message):
    return await message.reply("Soon...")

#[ ] /discounts_game                     — Знижки на ігри
@router.message(Command("discounts_game"))
async def discounts_game(message: Message):
    return await message.reply("Soon...")

#[ ] /most_played_games                  — Топ найпопулярніших ігор
@router.message(Command("most_played_games"))
async def most_played_games(message: Message):
    return await message.reply("Soon...")

#[ ] /games_for_you <user_id>/None                     — Індивідуальні рекомендації
@router.message(Command("search_game"))
async def search_game(message: Message):
    return await message.reply("Soon...")

#[ ] /discount_for_you <user_id>/None                  — Персональні знижки
@router.message(Command("search_game"))
async def search_game(message: Message):
    return await message.reply("Soon...")

#[ ] /achievements_game <gameID>         — Досягнення гри
@router.message(Command("achievements_game"))
async def achievements_game(message: Message):
    return await message.reply("Soon...")

#[ ] /check_game_price <назва гри>      — Моніторинг ціни
@router.message(Command("check_game_price"))
async def check_game_price(message: Message):
    return await message.reply("Soon...")

"""
Доволі важка функція буде створена в кінці самому з використанням ChatGPT API
"""
@router.message(Command("suggest_game"))
async def suggest_game(message: Message):
    return await message.reply("Soon...")
