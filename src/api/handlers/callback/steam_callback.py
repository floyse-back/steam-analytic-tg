from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import back_help_keyboard
from src.api.keyboards.steam.steam_dict_keyboards import steam_games_keyboards_dictionary
from src.api.keyboards.steam.steam_keyboards import create_page_swapper_inline, create_inline_steam_commands, \
    suggest_game_keyboard, create_search_share_keyboards, go_to_main_menu_inline_keyboard, create_player_steam_id
from src.api.presentation.steam_style_text import SteamStyleText
from src.api.utils.pages_utils import page_utils_elements
from src.api.utils.state import SteamGamesID, PlayerSteamName
from src.application.services.steam_service import SteamService
from src.infrastructure.db.database import get_async_db
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import steam_message_menu

router = Router()
steam_service = SteamService(
    steam_client=SteamAnalyticsAPIClient(),
    users_repository = UsersRepository()
)
steam_style_text = SteamStyleText()

#Callbacks
@router.callback_query(F.data == "games_help")
async def games_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{steam_service.steam_help()}",parse_mode=ParseMode.MARKDOWN,reply_markup=back_help_keyboard)
    await callback_query.answer()

@router.callback_query(F.data == "search_game")
async def search_game_callback(callback_query: CallbackQuery,state: FSMContext):
    await state.update_data(command ="search_game")
    await state.set_state(SteamGamesID.game)
    await callback_query.message.answer("Введіть назву гри:")
    await callback_query.answer()

@router.callback_query(lambda c: c.data.startswith("search_game"))
async def search_game_callback_pages(callback_query: CallbackQuery):
    callback_name = "".join(callback_query.data.split(":")[0:1])
    await callback_query.answer()
    page = page_utils_elements(callback_data=callback_query.data,page_one_data=callback_name,index=2)
    game =callback_query.data.split(":")[1]
    logger.debug("Game:%s,Page:%s",game,page)
    data = await steam_service.search_games(name=game,page=page,limit=5)
    response = steam_style_text.create_short_desc(data)
    logger.debug("data:%s",data)
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=create_page_swapper_inline(callback_data=f"search_game:{game}",current_page=page,menu_callback_data=f"steam_menu"))

@router.callback_query(lambda c: c.data.startswith("search_short_games"))
async def search_game_callback_pages_short(callback_query: CallbackQuery):
    callback_name = "".join(callback_query.data.split(":")[0:1])
    main_callback_name = callback_query.data.split(":")[2]
    await callback_query.answer()
    page = page_utils_elements(callback_data=callback_query.data, page_one_data=callback_name, index=3)
    game = callback_query.data.split(":")[1]
    logger.debug("Game:%s,Page:%s", game, page)
    data = await steam_service.search_games(name=game, page=page, limit=5,share=False)
    response = steam_style_text.create_short_search_games(data,page=page,limit=5)
    inline_board_new = create_search_share_keyboards(
                                               callback_data=f"{main_callback_name}",
                                               value=game,
                                               data=data,
                                               page=page
                                           )
    if data is None:
        await callback_query.message.edit_reply_markup(reply_markup=inline_board_new)
    else:
        await callback_query.message.edit_text(f"{response}", parse_mode=ParseMode.HTML,
                                           reply_markup=create_search_share_keyboards(
                                               callback_data=f"{main_callback_name}",
                                               value=game,
                                               data=data,
                                               page=page
                                           ))

@router.callback_query(F.data == "free_now")
async def free_games_now_callback(callback_query: CallbackQuery):
    data = await steam_service.free_games_now()
    response = steam_style_text.create_short_desc(data=data)
    await callback_query.message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=go_to_main_menu_inline_keyboard)
    await callback_query.answer()

@router.callback_query(F.data == "achievements_game")
async def achievements_game_callback_state(callback_query: CallbackQuery,state: FSMContext):
    await state.update_data(command="achievements_game")
    await state.set_state(SteamGamesID.game)
    await callback_query.message.answer("Введіть назву гри:")
    await callback_query.answer("Введіть назву гри")

@router.callback_query(lambda c: c.data.startswith("achievements_game"))
async def achievements_game_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    game = callback_query.data.split(":")[1]
    data = await steam_service.achievements_game(game=game)
    response = steam_style_text.create_achievements_description(data=data,game=game)
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=steam_games_keyboards_dictionary["achievements_game"])

@router.callback_query(lambda c:c.data.startswith("most_played_games"))
async def most_played_games_callback(callback_query: CallbackQuery):
    callback_name = "most_played_games"
    page = page_utils_elements(callback_data=callback_query.data, page_one_data=callback_name)

    data = await steam_service.most_played_games(page=page, limit=10)
    response = steam_style_text.create_short_list_games(data=data,page=page,limit=10)
    await callback_query.message.edit_text(f"{response}", parse_mode=ParseMode.HTML,
                                           reply_markup=create_page_swapper_inline(callback_data=callback_name,
                                                                                         menu_callback_data="steam_menu",
                                                                                         current_page=page))


@router.callback_query(lambda c:c.data.startswith("discount_games"))
async def discount_games_callback(callback_query: CallbackQuery):
    callback_name = "discount_games"
    page = page_utils_elements(callback_data=callback_query.data,page_one_data=callback_name)

    data = await steam_service.discount_games(page=page,limit=10)
    response = steam_style_text.create_short_list_games(data=data,limit=10,page=page)
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup= create_page_swapper_inline(callback_data=callback_name,menu_callback_data="steam_menu",current_page=page))

@router.callback_query(F.data == "games_for_you")
async def games_for_you_callback(callback_query:CallbackQuery,state: FSMContext):
    await state.update_data(command="games_for_you",text="🎮 Ігри для тебе")
    await state.set_state(PlayerSteamName.player)
    async for session in get_async_db():
        steam_appid = await steam_service.get_player(telegram_appid=callback_query.from_user.id,session=session)
        logger.debug("Steam Appid From Steam Service,%s",callback_query.message.from_user.id)
        logger.debug(f"steam_appid: {steam_appid}")
        await callback_query.message.answer("<b>Введіть назву користувача: </b>",parse_mode=ParseMode.HTML,reply_markup=create_player_steam_id(callback_data=callback_query.data,steam_appid=steam_appid))
    await callback_query.answer("Введіть ім'я користувача")

@router.callback_query(lambda c:c.data.startswith("games_for_you"))
async def games_for_you_callback_pages(callback_query: CallbackQuery):
    name,player,page = callback_query.data.split(":")
    logger.debug("Discount Params %s %s %s",name,player,page)
    data = await steam_service.games_for_you(user=player,page=int(page),limit=5)
    response = steam_style_text.create_for_you(data=data,player=player,page=int(page),limit=5)
    await callback_query.answer()
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=create_page_swapper_inline(
        callback_data=f"{name}:{player}", menu_callback_data="steam_menu", current_page=int(page),
        count=len(data)
    ))

@router.callback_query(F.data == "discount_for_you")
async def discount_for_you_callback(callback_query: CallbackQuery,state: FSMContext):
    await state.update_data(command="discount_for_you",text="💰 Знижки для тебе")
    await state.set_state(PlayerSteamName.player)
    async for session in get_async_db():
        steam_appid = await steam_service.get_player(telegram_appid=callback_query.from_user.id,session=session)
        logger.debug("Steam Appid From Steam Service,%s",callback_query.message.from_user.id)
        logger.debug(f"steam_appid: {steam_appid}")
    await callback_query.message.answer("<b>Введіть назву користувача: </b>",parse_mode=ParseMode.HTML,reply_markup=create_player_steam_id(callback_data=callback_query.data,steam_appid=steam_appid))
    await callback_query.answer("Введіть ім'я користувача")

@router.callback_query(lambda c:c.data.startswith("discount_for_you"))
async def discount_for_you_callback_pages(callback_query: CallbackQuery):
    name,player,page = callback_query.data.split(":")
    logger.debug("Discount Params %s %s %s",name,player,page)
    data = await steam_service.discount_for_you(user=player,page=int(page),limit=5)
    response = steam_style_text.create_for_you(data=data,player=player,page=int(page),limit=5)
    await callback_query.answer()
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=create_page_swapper_inline(
        callback_data=f"{name}:{player}", menu_callback_data="steam_menu", current_page=int(page),
        count=len(data)
    ))

@router.callback_query(F.data == "game_price")
async def game_price_callback_state(callback_query: CallbackQuery,state:FSMContext):
    await state.update_data(command="game_price")
    await state.set_state(SteamGamesID.game)
    await callback_query.message.answer("<b>Введіть назву гри:</b>",parse_mode=ParseMode.HTML)
    await callback_query.answer("Введіть назву гри")

@router.callback_query(lambda c: c.data.startswith("game_price"))
async def game_price_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    data =await steam_service.check_game_price(game=callback_query.data.split(":")[1])
    response = steam_style_text.create_game_price(data=data)
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=steam_games_keyboards_dictionary["game_price"])

@router.callback_query(F.data == "suggest_game")
async def suggest_game_callback(callback_query: CallbackQuery):
    data = await steam_service.suggest_game()
    await callback_query.message.edit_text(f"{steam_style_text.create_short_desc(data=data)}",parse_mode=ParseMode.HTML,reply_markup=suggest_game_keyboard)
    await callback_query.answer()

@router.callback_query(F.data == "steam_menu")
async def steam_menu_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    return await callback_query.message.edit_text(text=f"{steam_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_steam_commands())

@router.callback_query(F.data == "noop")
async def noop_callback(callback_query: CallbackQuery):
    return await callback_query.answer()
