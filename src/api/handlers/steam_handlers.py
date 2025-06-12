from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.api.keyboards.main_keyboards import back_help_keyboard
from src.api.keyboards.steam_keyboards import create_inline_steam_commands
from src.application.services.steam_service import SteamService
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import MainMenu, steam_message_menu
from src.api.utils.state import SteamGamesID

router = Router(name=__name__)

steam_service = SteamService(
    steam_client= SteamAnalyticsAPIClient()
)


@router.message(lambda message: message.text == f"{MainMenu.steam}")
async def steam_main(message: Message):
    await message.delete()
    await message.answer(text=f"{steam_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_steam_commands())

@router.message(Command(commands=["games"]))
async def help_command(message: Message):
    await message.delete()
    return await message.answer(steam_service.steam_help(),parse_mode=ParseMode.MARKDOWN)

# [ ] /search_game <назва>                — Пошук гри
@router.message(Command("search_game"))
async def search_game(message: Message):
    split_message = message.text.split()
    await message.delete()

    if len(split_message) < 2:
        return await message.answer("You need to specify a game name")

    data = await steam_service.search_games(name=split_message[1])
    await message.answer(f"{data}")

#[ ] /free_games_now                     — Актуальні безкоштовні ігри (Steam + Epic)
@router.message(Command("free_games_now"))
async def free_games_now(message: Message):
    await message.delete()

    data = await steam_service.free_games_now()
    await message.answer(f"{data}")

#[ ] /discounts_game                     — Знижки на ігри
@router.message(Command("discounts_game"))
async def discounts_game(message: Message):
    await message.delete()
    data = await steam_service.discount_games()
    print(data)
    await message.answer(f"{data}")

#[ ] /most_played_games                  — Топ найпопулярніших ігор
@router.message(Command("most_played_games"))
async def most_played_games(message: Message):
    await message.delete()

    data = await steam_service.most_played_games()
    await message.answer(f"{data}")

#[ ] /games_for_you <user_id>/None                     — Індивідуальні рекомендації
@router.message(Command("games_for_you"))
async def games_for_you(message: Message):
    split_message = message.text.split()

    if len(split_message) < 2:
        return await message.answer("You need to specify a game name")
    else:
        user = " ".join(split_message[1:])
    await message.delete()

    data = await steam_service.games_for_you(user=user)
    await message.answer(f"{data}")

#[ ] /discount_for_you <user_id>/None                  — Персональні знижки
@router.message(Command("discount_for_you"))
async def discount_for_you(message: Message):
    split_message = message.text.split()

    if len(split_message) < 2:
        return await message.answer("You need to specify a game name")
    else:
        user = " ".join(split_message[1:])
    await message.delete()

    data = await steam_service.discount_for_you(user=user)
    await message.answer(f"{data}")


#[ ] /achievements_game <gameID>         — Досягнення гри
@router.message(Command("achievements_game"))
async def achievements_game(message: Message):
    split_message = message.text.split()

    if len(split_message) < 2:
        return await message.answer("You need to specify a game name")
    else:
        game = " ".join(split_message[1:])
    await message.delete()

    data = await steam_service.achievements_game(game=game)
    await message.answer(f"{data}")


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

@router.message(SteamGamesID.game_id)
async def steam_game_name(message: Message,state: FSMContext):
    await state.update_data(game_id=message.text)
    data = await state.get_data()

    await state.clear()


#Callbacks
@router.callback_query(F.data == "games_help")
async def games_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{steam_service.steam_help()}",parse_mode=ParseMode.MARKDOWN,reply_markup=back_help_keyboard)
    await callback_query.answer()

@router.callback_query(F.data == "search_game")
async def search_game_callback(callback_query: CallbackQuery,state: FSMContext):
    await callback_query.message.answer(text="S",parse_mode=ParseMode.MARKDOWN)
    await state.set_state(SteamGamesID.game_id)
    await callback_query.message.answer("Введіть назву гри:")
    await callback_query.answer()