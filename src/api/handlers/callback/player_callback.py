from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.api.keyboards.player.player_keyboards import create_inline_player_commands, find_other_player
from src.api.keyboards.steam.steam_keyboards import create_player_steam_id
from src.api.presentation.player_style_text import PlayerStyleText
from src.api.utils.state import SteamPlayerName, BattleSteamPlayer
from src.application.services.player_service import PlayerService
from src.infrastructure.db.database import get_async_db
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import player_message_menu

router = Router()

player_service = PlayerService(
    steam_client=SteamAnalyticsAPIClient(),
    users_repository=UsersRepository(),
)
player_style_text = PlayerStyleText()

@router.callback_query(lambda c: c.data in ["player_badges","player_full_stats","player_rating","player_play"])
async def player_one_user_callback(callback_query:CallbackQuery,state:FSMContext):
    logger.debug("Callback_query %s",callback_query.data)
    callback_data = callback_query.data
    await state.update_data(command = callback_data,last_bot_message_id=callback_query.message.message_id)
    await state.set_state(SteamPlayerName.player)
    async for session in get_async_db():
        steam_appid = await player_service.get_user_steam_id(telegram_id=callback_query.from_user.id,session=session)
    logger.info("Steam appid: %s",steam_appid)
    await callback_query.answer()
    await callback_query.message.edit_text(f"{player_style_text.create_message_from_get_user()}",parse_mode=ParseMode.HTML,reply_markup=create_player_steam_id(steam_appid=steam_appid,callback_data=callback_data,page=""))

@router.callback_query(lambda c: any(c.data.startswith(i) for i in [
    "player_badges", "player_full_stats", "player_rating", "player_play"
]))
async def player_one_user_callback_between(callback_query:CallbackQuery,state:FSMContext):
    player = callback_query.data.split(":")[1]
    callback_data_name = callback_query.data.split(":")[0]
    logger.debug("Callback_query %s",callback_query.data)
    data = await player_service.dispatcher(callback_data_name,player)
    response = player_style_text.dispatcher(callback_data_name,data)
    await state.clear()
    await callback_query.message.edit_text(text=f"{response}",parse_mode=ParseMode.HTML,reply_markup=find_other_player(callback_data=callback_data_name))
    await callback_query.answer()

@router.callback_query(F.data=="compare_users")
async def compare_users_callback(callback_query: CallbackQuery,state:FSMContext):
    logger.debug("Callback_query %s",callback_query.data)
    await state.set_state(BattleSteamPlayer.user_1)
    steam_appid = None
    async for session in get_async_db():
        steam_appid = await player_service.get_user_steam_id(telegram_id=callback_query.from_user.id,session=session)
        if steam_appid:
            await state.update_data(steam_appid=steam_appid)
    await callback_query.message.edit_text(f"{player_style_text.create_message_from_get_user()}",parse_mode=ParseMode.HTML,reply_markup=create_player_steam_id(steam_appid=steam_appid,callback_data=f"{callback_query.data}",page=""))
    await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith("compare_users"))
async def compare_users_callback_between(callback_query: CallbackQuery,state:FSMContext):
    logger.debug("Callback_query %s",callback_query.data)
    state_data = await state.get_data()
    player = callback_query.data.split(":")[1]
    await  callback_query.answer()
    if state_data.get("user1") is None:
        await state.update_data(user1=player,complited=True)
        await state.set_state(BattleSteamPlayer.user_2)
        await callback_query.message.edit_text(f"{player_style_text.create_message_from_get_user(users=1)}",parse_mode=ParseMode.HTML)
    elif state_data.get("user2") is None:
        data = await player_service.get_player_battle(user1=state_data['user1'],user2=player)
        response = player_style_text.get_player_compare(data=data)
        await state.clear()
        await callback_query.message.edit_text(response,parse_mode=ParseMode.HTML,reply_markup=find_other_player(callback_data="compare_users"))

@router.callback_query(F.data == "player_menu")
async def player_main(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(text=f"{player_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_player_commands())

@router.callback_query(F.data == "player_menu_callback_close")
async def player_main(callback_query: CallbackQuery,state:FSMContext):
    state_data = await state.get_data()
    if state_data.get("last_bot_message_id") is not None:
        await callback_query.message.bot.delete_message(message_id=state_data["last_bot_message_id"],chat_id=callback_query.message.chat.id)
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer(text=f"{player_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_player_commands())
