from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.api.keyboards.main_keyboards import back_help_keyboard
from src.api.utils.state import SteamGamesID
from src.application.services.steam_service import SteamService
from src.infrastructure.steam_analytic_api.steam_client import SteamAnalyticsAPIClient

router = Router()
steam_service = SteamService(
    steam_client=SteamAnalyticsAPIClient()
)

#Callbacks
@router.callback_query(F.data == "games_help")
async def games_help_callback(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{steam_service.steam_help()}",parse_mode=ParseMode.MARKDOWN,reply_markup=back_help_keyboard)
    await callback_query.answer()

@router.callback_query(F.data == "search_game")
async def search_game_callback(callback_query: CallbackQuery,state: FSMContext):
    await state.update_data(command ="search_game")
    await state.set_state(SteamGamesID.game)
    await callback_query.message.answer("Введіть назву гри:")
    await callback_query.answer()

@router.callback_query(F.data == "free_now")
async def free_games_now_callback(callback_query: CallbackQuery):
    data = await steam_service.free_games_now()
    await callback_query.message.answer(f"{data}",parse_mode=ParseMode.MARKDOWN)
    await callback_query.answer()

@router.callback_query(F.data == "achievements_game")
async def achievements_game_callback(callback_query: CallbackQuery,state: FSMContext):
    await state.update_data(command="achievements_game")
    await state.set_state(SteamGamesID.game)
    await callback_query.answer("Введіть назву гри")
    await callback_query.answer()

@router.callback_query(F.data == "most_played_games")
async def most_played_games_callback(callback_query: CallbackQuery):
    data=await steam_service.most_played_games()
    await callback_query.answer(f"{data}",parse_mode=ParseMode.MARKDOWN)

@router.callback_query(F.data == "games_for_you")
async def games_for_you_callback(callback_query:CallbackQuery,state: FSMContext):
    await callback_query.message.answer("Soon...")
    await callback_query.answer()

@router.callback_query(F.data == "discount_for_you")
async def discount_for_you_callback(callback_query: CallbackQuery,state: FSMContext):
    await callback_query.message.answer("Soon...")
    await callback_query.answer()

@router.callback_query(F.data == "game_price")
async def game_price_callback(callback_query: CallbackQuery):
    await callback_query.message.answer("Soon...")
    await callback_query.answer()

@router.callback_query(F.data == "suggest_game")
async def suggest_game_callback(callback_query: CallbackQuery):
    await callback_query.message.answer("Soon...")
    await callback_query.answer()