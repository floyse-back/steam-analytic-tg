from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from src.api.keyboards.subscribes.subscribe_keyboards import create_inline_subscribes_commands
from src.application.services.subscribe_service import SubscribeService
from src.infrastructure.db.repository.users_repository import UsersRepository
from src.shared.config import MainMenu, subscribes_message_menu

router = Router(name=__name__)
subscribe_service = SubscribeService(
    users_repository=UsersRepository()
)

@router.message(lambda message: message.text == f"{MainMenu.subscribes}")
async def subscribes_main(message: Message):
    await message.delete()
    await message.answer(text=f"{subscribes_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_subscribes_commands())

