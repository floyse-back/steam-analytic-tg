from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.users.users_keyboards import create_user_inline_keyboard, \
    back_to_profile_main, profile_cancel_inline_keyboard_main, create_wishlist_inline_keyboard, \
    create_remove_wishlist_inline_keyboard, go_to_wishlist_inline_keyboard
from src.api.presentation.users_style_text import UsersStyleText
from src.api.utils.pages_utils import page_utils_elements
from src.api.utils.state import ProfileSteamName, ChangeSteamName, WishlistGame
from src.application.services.users_service import UsersService
from src.infrastructure.db.database import get_async_db
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.db.repository.wishlist_repository import WishlistRepository
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import user_message_menu

router = Router()

users_service = UsersService(
    users_repository=UsersRepository(),
    steam_client=SteamAnalyticsAPIClient(),
    wishlist_repository=WishlistRepository(),
)
users_style_text = UsersStyleText()

@router.callback_query(lambda c: c.data.startswith("wishlist"))
async def wishlist_callback(callback_query: CallbackQuery):
    page = page_utils_elements(callback_data=callback_query.data,page_one_data="wishlist",index=1)
    async for session in get_async_db():
        data = await users_service.show_wishlist_games(user_id=callback_query.from_user.id,session=session,page=page,limit=5)
        response = users_style_text.create_short_wishlist_message(data=data)
    if data is None and page !=1:
        await callback_query.message.edit_reply_markup(
            reply_markup=create_wishlist_inline_keyboard(
            callback_data="wishlist",
            current_page=page-1,
            count=0,
            limit=5,
        ),
        )
    else:
        await callback_query.message.edit_text(
            f"<b>Ваші улюблені ігри:</b>\n\n{response}",
            parse_mode=ParseMode.HTML,
            reply_markup=create_wishlist_inline_keyboard(
            callback_data="wishlist",
            current_page=page,
            count=len(data),
            limit=5,
            next_page=None
        ),
    )
    await callback_query.answer()

@router.callback_query(lambda c:c.data=="add_wishlist_game")
async def add_wishlist_game_callback(callback_query: CallbackQuery,state:FSMContext):
    await state.clear()
    await state.update_data(command="add_wishlist_game")
    await state.set_state(WishlistGame.game)
    await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(f"{users_style_text.message_post_game()}",parse_mode=ParseMode.HTML,reply_markup=go_to_wishlist_inline_keyboard)
    await callback_query.answer()

@router.callback_query(lambda c:c.data.startswith("add_wishlist_game"))
async def add_wishlist_game_callback_confirmation(callback_query: CallbackQuery):
    game = callback_query.data.split(":")[1]
    logger.debug("Callback Data Name: %s", callback_query.data)
    async for session in get_async_db():
        data = await users_service.add_wishlist_game(game=int(game),user_id=callback_query.from_user.id,session=session)
    if data:
        text = users_style_text.message_correct_add_game()
        reply_markup = None
    else:
        text = users_style_text.message_incorrect_add_game()
        reply_markup = None
    await callback_query.answer()
    await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

@router.callback_query(lambda c:c.data.startswith("remove_wishlist_game"))
async def remove_wishlist_game_callback(callback_query: CallbackQuery):
    page = page_utils_elements(callback_data=callback_query.data, page_one_data="remove_wishlist_game", index=1)
    async for session in get_async_db():
        data = await users_service.show_wishlist_games(user_id=callback_query.from_user.id, session=session, page=page,
                                                       limit=5)
        response = users_style_text.create_short_wishlist_message(data=data)
    if data is None and page != 1:
        next_page = True
    else:
        next_page = None
    lenght_data =len(data) if isinstance(data, list) else 0
    await callback_query.message.edit_text(
        f"<b>Ваші улюблені ігри:</b>\n\n{response}",
        parse_mode=ParseMode.HTML,
        reply_markup=create_remove_wishlist_inline_keyboard(
            data=data,
            callback_data="remove_wishlist_game",
            delete_call_start_data = "remove_wishlist_appid_games",
            current_page=page,
            count=lenght_data,
            limit=5,
            next_page=next_page,
            user_id=callback_query.from_user.id
        ),
    )

@router.callback_query(lambda c:c.data.startswith("remove_wishlist_appid_games"))
async def remove_wishlist_game_callback_confirmation(callback_query: CallbackQuery):
    logger.debug("Callback Data Name: %s", callback_query.data)
    game_id = callback_query.data.split(":")[1]
    user_id = callback_query.data.split(":")[2]
    await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    async for session in get_async_db():
        if await users_service.remove_wishlist_game(user_id=int(user_id),session=session,game_id=int(game_id)):
            return await callback_query.message.answer(f"{users_style_text.game_correct_delete_wishlist(user=callback_query.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=go_to_wishlist_inline_keyboard)
        else:
            return await callback_query.message.answer(f"{users_style_text.game_not_delete_wishlist(user=callback_query.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=go_to_wishlist_inline_keyboard)


@router.callback_query(F.data=="profile")
async def profile_callback(callback_query: CallbackQuery,state: FSMContext):
    await callback_query.answer()
    data = None
    async for session in get_async_db():
        data = await users_service.get_profile_user(telegram_id=callback_query.from_user.id,session=session)
    if data is None or data == False:
        await state.update_data()
        await state.set_state(ProfileSteamName.profile)
        await callback_query.message.answer(f"{users_style_text.message_no_steam_id(username=callback_query.message.from_user.username)}",
                             parse_mode=ParseMode.HTML, reply_markup=start_keyboard)
        return None
    response = users_style_text.get_player_full_stats(data=data)
    await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(f"{response}",parse_mode=ParseMode.HTML,reply_markup=back_to_profile_main)

@router.callback_query(F.data=="user_steam_info")
async def user_message_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="change_my_id")
async def change_id_callback(callback_query: CallbackQuery,state: FSMContext):
    await state.set_state(ChangeSteamName.steam_appid_new)
    await state.update_data(last_bot_message_id=callback_query.message.message_id)
    await callback_query.bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await callback_query.message.answer(f"{users_style_text.message_change_steam_id(username=callback_query.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=profile_cancel_inline_keyboard_main)
    await callback_query.answer()

@router.callback_query(F.data == "user_main")
async def user_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{user_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_user_inline_keyboard())
    await callback_query.answer()

@router.callback_query(F.data =="profile_cancel_state")
async def profile_cancel_callback(callback_query: CallbackQuery,state:FSMContext):
    await state.clear()
    await callback_query.message.delete()
    await callback_query.message.answer(f"Добре оберіть розділ який вас цікавить!",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)
    await callback_query.answer()