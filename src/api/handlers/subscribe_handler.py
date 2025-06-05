from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command

from src.application.services.subscribe_service import SubscribeService

router = Router(name=__name__)
subscribe_service = SubscribeService()

@router.message(Command("games"))
async def help_command(message: Message):
    await message.delete()
    return await message.answer(subscribe_service.subscribe_help(),parse_mode=ParseMode.MARKDOWN)


# [ ] /subscribe_new_release <True/False>             — Нові релізи
@router.message(Command("subscribe_new_release"))
async def subscribe_new_release(message: Message):
    return await message.answer("Soon...")

# [ ] /subscribe_free_games <True/False>              — Безкоштовні ігри
@router.message(Command("subscribe_free_games"))
async def subscribe_free_games(message: Message):
    return await message.answer("Soon...")

# [ ] /subscribe_new_event <True/False>               — Події Steam
@router.message(Command("subscribe_new_event"))
async def subscribe_new_event(message: Message):
    return await message.answer("Soon...")

# [ ] /subscribe_steam_news <True/False>              — Новини Steam
@router.message(Command("subscribe_steam_news"))
async def subscribe_steam_news(message: Message):
    return await message.answer("Soon...")

# [ ] /subscribe_steam_update <True/False>            — Оновлення Steam
@router.message(Command("subscribe_steam_update"))
async def subscribe_steam_update(message: Message):
    return await message.answer("Soon...")
# [ ] /subscribe_whishlist_notificate <True/False>    — Знижки у wishlist
@router.message(Command("subscribe_whishlist_notificate"))
async def subscribe_whishlist_notificate(message: Message):
    return await message.answer("Soon...")

# [ ] /subscribe_hot_discount_notificate <True/False> — Гарячі знижки
@router.message(Command("subscribe_hot_discount_notificate"))
async def subscribe_hot_discount_notificate(message: Message):
    return await message.answer("Soon...")
