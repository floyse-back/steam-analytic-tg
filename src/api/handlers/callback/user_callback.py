from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import back_help_keyboard
from src.api.keyboards.users.users_keyboards import wishlist_inline_keyboard_main, create_user_inline_keyboard
from src.application.services.users_service import UsersService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.shared.config import user_message_menu

router = Router()

users_service = UsersService(
    users_repository=UsersRepository()
)

@router.callback_query(F.data=="profile")
async def profile_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="whishlist")
async def wishlist_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Ваші улюблені ігри:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=wishlist_inline_keyboard_main,
    )
    await callback_query.answer()

@router.callback_query(F.data=="profile")
async def profile_callback(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(

    )

@router.callback_query(F.data=="user_steam_info")
async def user_message_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="user_message_menu")
async def change_id_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data == "user_main")
async def user_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{user_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_user_inline_keyboard())
    await callback_query.answer()
