from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import back_help_keyboard
from src.api.utils.state import PlayerSteamName, SteamPlayerName
from src.application.services.player_service import PlayerService
from src.infrastructure.logging.logger import logger
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient

router = Router()

player_service = PlayerService(
    steam_client=SteamAnalyticsAPIClient(),
)

@router.callback_query(F.data == "player_help")
async def player_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{player_service.player_help()}",parse_mode=ParseMode.MARKDOWN,reply_markup=back_help_keyboard)
    await callback_query.answer()

@router.callback_query(lambda c: c.data in ["player_badges","player_full_stats","player_rating","player_play"])
async def player_one_user_callback(callback_query:CallbackQuery,state:FSMContext):
    logger.debug("Callback_query %s",callback_query.data)
    await state.update_data(command = f"{callback_query.data}")
    await state.set_state(SteamPlayerName.player)
    await callback_query.answer()
    await callback_query.message.answer("<b>Введіть будь ласка ваш SteamAPPID</b>")


