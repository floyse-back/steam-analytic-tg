from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.api.keyboards.subscribes.subscribe_keyboards import create_inline_subscribes_commands
from src.api.middleware.account import user_get_or_none
from src.api.middleware.message_delete import message_delete
from src.shared.config import MainMenu, subscribes_message_menu
from src.shared.depends import get_users_service, get_subscribes_service

router = Router(name=__name__)
subscribe_service = get_subscribes_service()
users_service = get_users_service()

@router.message(lambda message: message.text == f"{MainMenu.subscribes}")
async def subscribes_main(message: Message,state: FSMContext):
    if await user_get_or_none(state=state,telegram_id=message.from_user.id,message=message,users_service=users_service) is None:
        return None
    await message_delete(message=message,state=state)
    await message.delete()
    await message.answer(text=f"{subscribes_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_subscribes_commands())

