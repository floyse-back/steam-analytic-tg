from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.api import keyboards
from src.api.keyboards.main_keyboards import start_keyboard
from src.api.keyboards.users.users_keyboards import wishlist_inline_keyboard_main, create_user_inline_keyboard, \
    back_to_profile_main, profile_cancel_inline_keyboard_main
from src.api.presentation.users_style_text import UsersStyleText
from src.api.utils.state import ProfileSteamName, ChangeSteamName
from src.application.services.users_service import UsersService
from src.infrastructure.db.database import get_async_db
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import user_message_menu

router = Router()

users_service = UsersService(
    users_repository=UsersRepository(),
    steam_client=SteamAnalyticsAPIClient(),
)
users_style_text = UsersStyleText()

@router.callback_query(F.data=="wishlist")
async def wishlist_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Ваші улюблені ігри:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=wishlist_inline_keyboard_main,
    )
    await callback_query.answer()

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
    await callback_query.message.edit_text(f"{response}",parse_mode=ParseMode.HTML,reply_markup=back_to_profile_main)

@router.callback_query(F.data=="user_steam_info")
async def user_message_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="change_my_id")
async def change_id_callback(callback_query: CallbackQuery,state: FSMContext):
    await state.set_state(ChangeSteamName.steam_appid_new)
    await state.update_data(last_bot_message_id=callback_query.message.message_id)
    await callback_query.message.edit_text(f"{users_style_text.message_change_steam_id(username=callback_query.from_user.username)}",parse_mode=ParseMode.HTML,reply_markup=profile_cancel_inline_keyboard_main)
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