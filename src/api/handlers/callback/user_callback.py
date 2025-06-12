from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

router = Router()

@router.callback_query(F.data=="profile")
async def profile_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="whishlist")
async def whish_list_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="user_steam_info")
async def user_message_callback(callback_query: CallbackQuery):
    await callback_query.answer()

@router.callback_query(F.data=="user_message_menu")
async def change_id_callback(callback_query: CallbackQuery):
    await callback_query.answer()


