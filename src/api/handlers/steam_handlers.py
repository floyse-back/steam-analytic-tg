from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.keyboards.steam.steam_dict_keyboards import steam_games_keyboards_dictionary
from src.api.keyboards.steam.steam_keyboards import create_inline_steam_commands, \
    create_player_details_inline, create_page_swapper_inline, create_search_share_keyboards, \
    go_to_main_menu_inline_keyboard
from src.api.presentation.steam_style_text import SteamStyleText
from src.application.services.steam_service import SteamService
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import MainMenu, steam_message_menu
from src.api.utils.state import SteamGamesID, PlayerSteamName

router = Router(name=__name__)

steam_service = SteamService(
    steam_client= SteamAnalyticsAPIClient()
)

steam_style_text = SteamStyleText()

@router.message(lambda message: message.text == f"{MainMenu.steam}")
async def steam_main(message: Message):
    await message.delete()
    await message.answer(text=f"{steam_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_steam_commands())

@router.message(Command(commands=["games"]))
async def help_command(message: Message):
    await message.delete()
    return await message.answer(steam_service.steam_help(),parse_mode=ParseMode.MARKDOWN)

#[ ] /free_games_now                     — Актуальні безкоштовні ігри (Steam + Epic)
@router.message(Command("free_games_now"))
async def free_games_now(message: Message):
    await message.delete()

    data = await steam_service.free_games_now()
    response = steam_style_text.create_short_desc(data=data)
    await message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=go_to_main_menu_inline_keyboard)

#[ ] /discounts_game                     — Знижки на ігри
@router.message(Command("discounts_game"))
async def discounts_game(message: Message):
    await message.delete()
    data = await steam_service.discount_games()
    await message.answer(f"{data}",parse_mode=ParseMode.MARKDOWN)

#[ ] /most_played_games                  — Топ найпопулярніших ігор
@router.message(Command("most_played_games"))
async def most_played_games(message: Message):
    await message.delete()

    data = await steam_service.most_played_games()
    await message.answer(f"{data}",parse_mode=ParseMode.MARKDOWN)

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

    data = await steam_service.achievements_game(game=game,page=1,offset=10)
    await message.answer(f"{data}",parse_mode=ParseMode.MARKDOWN)


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

@router.message(SteamGamesID.game)
async def steam_game_name(message: Message,state: FSMContext):
    page,limit=1,5
    await state.update_data(game=message.text)
    data = await state.get_data()
    if data["command"]!="search_game":
        new_data = await steam_service.search_games(name=data["game"],page=page,limit=limit,share=False)
        response = steam_style_text.create_short_search_games(new_data,page=page,limit=limit)
        logger.debug("Response: %s",response)
        if not new_data is None:
            reply_command = create_search_share_keyboards(callback_data=data["command"],value=data["game"],data=new_data,page=page,limit=limit)
    else:
        new_data = await steam_service.search_games(name=data["game"],page=page,limit=limit)
        response = steam_style_text.create_short_desc(data=new_data)
        if not new_data is None:
            reply_command = create_page_swapper_inline(callback_data=f"search_game:{data['game']}",menu_callback_data="steam_menu",current_page=page)

    if new_data is not None and len(new_data)==1:
        response = await steam_service.dispatcher(data["command"], data["game"])
        reply_command=steam_games_keyboards_dictionary[f'{data["command"]}']

    logger.debug("Handler {%s}",response)
    await state.clear()

    await message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=reply_command)

@router.message(PlayerSteamName.player)
async def steam_player_name_or_id(message: Message,state: FSMContext):
    await state.update_data(player=message.text)
    data = await state.get_data()
    response = await steam_service.dispatcher(data["command"],data["player"])
    await state.clear()
    await message.answer(f"{response}",parse_mode=None,reply_markup=await create_player_details_inline(data["command"],data["text"]))