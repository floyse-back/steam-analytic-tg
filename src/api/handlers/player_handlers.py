from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from src.api.keyboards.player.player_keyboards import create_inline_player_commands
from src.api.utils.state import SteamPlayerName

from src.application.services.player_service import PlayerService
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient
from src.shared.config import MainMenu, player_message_menu

router = Router(name=__name__)

player_service = PlayerService(
    steam_client=SteamAnalyticsAPIClient(),
)

@router.message(Command("player"))
async def player_help(message: Message):
    await message.delete()
    return await message.answer(player_service.player_help(),parse_mode=ParseMode.MARKDOWN)

@router.message(lambda message: message.text == f"{MainMenu.player}")
async def player_main(message: Message):
    await message.delete()
    await message.answer(text=f"{player_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_player_commands())

@router.message(SteamPlayerName.player)
async def player_one_main(message: Message,state: FSMContext):
    await state.update_data(user=message.text)
    await message.delete()
    state_data = await state.get_data()
    data = await player_service.dispatcher(state_data['command'],state_data['user'])
    await state.clear()
    await message.answer(text=f"{data}",parse_mode=None)