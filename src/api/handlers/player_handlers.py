from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from src.api.keyboards.player.player_keyboards import create_inline_player_commands, find_other_player
from src.api.keyboards.steam.steam_keyboards import create_player_steam_id
from src.api.presentation.player_style_text import PlayerStyleText
from src.api.utils.state import SteamPlayerName, BattleSteamPlayer
from src.application.dto.users_dto import SteamVanityNameCorrection

from src.application.services.player_service import PlayerService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import MainMenu, player_message_menu

router = Router(name=__name__)

player_service = PlayerService(
    steam_client=SteamAnalyticsAPIClient(),
    users_repository=UsersRepository(),
)
player_style_text = PlayerStyleText()


@router.message(Command("player"))
async def player_help(message: Message):
    await message.delete()
    return await message.answer(player_service.player_help(),parse_mode=ParseMode.MARKDOWN)

@router.message(lambda message: message.text == f"{MainMenu.player}")
async def player_main(message: Message):
    await message.delete()
    await message.answer(text=f"{player_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_player_commands())

@router.message(SteamPlayerName.player)
async def player_one_main(message: Message,state: FSMContext):
    steam_message_correct = SteamVanityNameCorrection(steam_appid = message.text)
    data = await player_service.get_vanity_user(steam_message_correct.steam_appid)
    if data is None:
        await state.set_state(SteamPlayerName.player)
        return await message.answer(
            text=f"{player_style_text.create_incorrect_message_from_get_user(message.text)}",
            parse_mode=ParseMode.HTML,
            )
    await state.update_data(user=data['steam_appid'])
    await message.delete()
    state_data = await state.get_data()
    data = await player_service.dispatcher(state_data['command'],state_data['user'])
    response = player_style_text.dispatcher(state_data['command'],data=data)
    await state.clear()
    await message.bot.delete_message(message.chat.id, state_data['last_bot_message_id'])
    await message.answer(text=f"{response}",parse_mode=ParseMode.HTML,reply_markup=find_other_player(callback_data=state_data['command']))

@router.message(BattleSteamPlayer.user_1)
async def player_user_1(message: Message,state: FSMContext):
    steam_message_correct = SteamVanityNameCorrection(
        steam_appid = message.text
    )
    data = await player_service.get_vanity_user(steam_message_correct.steam_appid)

    state_data = await state.get_data()
    reply_markup = None
    if state_data.get("steam_appid") is not None and state_data.get("complited") is None:
        reply_markup = create_player_steam_id(callback_data='compare_users', steam_appid=state_data["steam_appid"],
                                              page="")
    if data is not None:
        await state.update_data(user1=data['steam_appid'])
        if data.get('steam_appid') == state_data.get('steam_appid'):
            await state.update_data(complited=True)
        await state.set_state(BattleSteamPlayer.user_2)
        await message.answer(text=f"{player_style_text.create_message_from_get_user()}",parse_mode=ParseMode.HTML,reply_markup=reply_markup)
    else:

        await state.set_state(BattleSteamPlayer.user_1)
        await message.answer(text=f"{player_style_text.create_incorrect_message_from_get_user(user=message.text)}",parse_mode=ParseMode.HTML,reply_markup=reply_markup)

@router.message(BattleSteamPlayer.user_2)
async def player_user_2(message: Message,state: FSMContext):
    steam_message_correct = SteamVanityNameCorrection(
        steam_appid = message.text
    )
    correct_user = await player_service.get_vanity_user(steam_message_correct.steam_appid)
    data = await state.get_data()
    logger.info("Return Player_User_2 data %s,correct_user %s",data,correct_user)
    if correct_user is None or str(correct_user.get("steam_appid")) == data['user1']:
        reply_markup = None
        if data.get("complited") is None and data['steam_appid'] is not None:
            reply_markup = create_player_steam_id(callback_data='compare_users',steam_appid=data["steam_appid"],page="")
        await state.set_state(BattleSteamPlayer.user_2)
        return await message.answer(text=f"{player_style_text.create_incorrect_message_from_get_user(user=message.text)}",parse_mode=ParseMode.HTML,reply_markup=reply_markup)

    await state.update_data(user2=correct_user['steam_appid'])
    users = await state.get_data()
    await state.clear()
    data = await player_service.get_player_battle(user1=users['user1'],user2=users['user2'])
    response = player_style_text.get_player_compare(data)
    await message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=find_other_player(callback_data="compare_users"))