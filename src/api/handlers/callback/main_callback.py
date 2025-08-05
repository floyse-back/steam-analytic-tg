from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ChatMemberBanned, ChatMemberLeft

from src.api.keyboards.main_keyboards import start_keyboard
from src.api.middleware.keyboards import check_subscribe, start_command_use
from src.api.presentation.main_style_text import MainStyleText
from src.shared.config import CHAT_ID, CHANNEL_URL

router = Router()

@router.callback_query(lambda c:c.data =="chose_category")
async def chose_category_answer(callback_query:CallbackQuery,state:FSMContext):
    await callback_query.answer()
    await callback_query.message.delete()
    new_message = await callback_query.message.answer(
        "<b>🎮 Виберіть одну з категорій нижче 👇</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=start_keyboard
    )
    await state.clear()
    await state.update_data(message_id=new_message.message_id,chat_id=new_message.chat.id)

@router.callback_query(lambda c:c.data =="check_subscribe")
async def check_subscribe_answer(callback_query:CallbackQuery):
    checker = await callback_query.bot.get_chat_member(chat_id=CHAT_ID, user_id=callback_query.from_user.id)
    await callback_query.message.delete()
    if isinstance(checker, (ChatMemberLeft, ChatMemberBanned)):
        response = MainStyleText().subscribe_channel(channel_url=CHANNEL_URL)
        await callback_query.message.answer(text=response, parse_mode=ParseMode.HTML,
                                              reply_markup=check_subscribe)
        await callback_query.answer()
    else:
        await callback_query.message.answer("Введіть ще раз /start",parse_mode=ParseMode.HTML,reply_markup=start_command_use)
        await callback_query.answer()
