from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import back_help_keyboard
from src.application.services.player_service import PlayerService

router = Router()

player_service = PlayerService()

@router.callback_query(F.data == "player_help")
async def player_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{player_service.player_help()}",parse_mode=ParseMode.MARKDOWN,reply_markup=back_help_keyboard)
    await callback_query.answer()
