from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.keyboards.steam.steam_dict_keyboards import steam_games_keyboards_dictionary
from src.api.keyboards.steam.steam_keyboards import create_inline_steam_commands, \
    create_page_swapper_inline, create_search_share_keyboards
from src.api.middleware.message_delete import message_delete
from src.api.presentation.steam_style_text import SteamStyleText
from src.application.dto.steam_dto import GameAppidValidatedModel
from src.application.dto.users_dto import SteamVanityNameCorrection
from src.infrastructure.logging.logger import Logger
from src.shared.config import MainMenu, steam_message_menu
from src.api.utils.state import SteamGamesID, PlayerSteamName
from src.shared.depends import get_steam_service

router = Router(name=__name__)

steam_service = get_steam_service()
logger = Logger(name="api.player_callback",file_path="api")
steam_style_text = SteamStyleText(logger=logger)

@router.message(lambda message: message.text == f"{MainMenu.steam}")
async def steam_main(message: Message,state: FSMContext):
    await message_delete(message=message,state=state)
    await message.delete()
    await message.answer(text=f"{steam_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_steam_commands())

@router.message(SteamGamesID.game)
async def steam_game_name(message: Message, state: FSMContext):
    page,limit=1,5
    app = GameAppidValidatedModel(
        steam_appid=message.text
    )
    await state.update_data(game=app.steam_appid)
    data = await state.get_data()
    reply_command = steam_games_keyboards_dictionary.get(f'{data['command']}')
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
            reply_command = create_page_swapper_inline(callback_data=f"search_game:{data['game']}",menu_callback_data="steam_menu",current_page=page,limit=limit,count=len(new_data))

    if new_data is not None and len(new_data)==1 and data["command"]!="search_game":
        answer = await steam_service.dispatcher(data["command"], data["game"])
        logger.debug("Response: %s  ,Command:%s",answer,data["command"])
        response = steam_style_text.dispatcher(data["command"],answer)
        reply_command=steam_games_keyboards_dictionary[f'{data["command"]}']

    logger.debug("Handler {%s}",response)
    await state.clear()
    try:
        await message.bot.delete_message(message.chat.id, data['last_bot_message_id'])
    except TelegramBadRequest as tbr:
        logger.critical("Chat ID %s,message %s Error Info:%s",message.chat.id,data['last_bot_message_id'],tbr.message)
    await message.delete()
    await message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=reply_command)

@router.message(PlayerSteamName.player)
async def steam_player_name_or_id(message: Message,state: FSMContext):
    steam_vanity = SteamVanityNameCorrection(steam_appid=message.text)
    await state.update_data(player=steam_vanity.steam_appid)
    data = await state.get_data()
    steam_data = await steam_service.dispatcher(data["command"],data["player"])
    logger.debug("Response: %s,Data: %s",steam_data,data)
    response = steam_style_text.dispatcher(data["command"],steam_data)
    await state.clear()
    try:
        await message.bot.delete_message(message.chat.id, data['last_bot_message_id'])
    except TelegramBadRequest as tbr:
        logger.critical("Chat ID %s,message %s Error Info:%s",message.chat.id,data['last_bot_message_id'],tbr.message)
    await message.delete()
    await message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=create_page_swapper_inline(callback_data=f"{data['command']}:{data['player']}",menu_callback_data="steam_menu",current_page=1,count=len(steam_data)))
