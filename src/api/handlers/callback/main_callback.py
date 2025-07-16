from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import start_keyboard

router = Router()

@router.callback_query(lambda c:c.data =="chose_category")
async def chose_category_answer(callback_query:CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    await callback_query.message.answer("<b>Виберіть категорію</b>",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)