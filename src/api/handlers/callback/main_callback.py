import asyncio
from csv import excel

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import AiogramError
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import start_keyboard
from src.infrastructure.logging.logger import logger

router = Router()

@router.callback_query(lambda c:c.data =="chose_category")
async def chose_category_answer(callback_query:CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    new_message = await callback_query.message.answer("<b>Виберіть категорію</b>",parse_mode=ParseMode.HTML,reply_markup=start_keyboard)
    await asyncio.sleep(5)
    try:
        await callback_query.bot.delete_message(message_id=new_message.message_id,chat_id=new_message.chat.id)
    except AiogramError as e:
        logger.critical("Message deleted %s",e)