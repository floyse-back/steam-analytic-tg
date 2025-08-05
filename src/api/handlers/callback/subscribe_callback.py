from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from src.api.keyboards.subscribes.subscribe_keyboards import create_inline_subscribes_commands, \
    create_subscribes_keyboard, create_unsubscribes_keyboard, inline_back_subscribe_menu
from src.api.presentation.subscribe_style_text import SubscribeStyleText
from src.api.utils.sub_utils import subscribe_correct
from src.infrastructure.db.database import get_async_db
from src.infrastructure.logging.logger import Logger
from src.shared.config import subscribes_message_menu
from src.shared.depends import get_subscribes_service
from src.shared.subscribe_types import SUBSCRIBES_TYPE_DATA_REVERSE, SUBSCRIBES_TYPE_DATA

router = Router()
logger = Logger(name="api.subscribe_callback",file_path="api")

subscribes_list = [i for i in list(SUBSCRIBES_TYPE_DATA.values())]
subscribes_service = get_subscribes_service()

subscribes_style_text = SubscribeStyleText(
    logger=Logger(name="api.subscribe_style_text",file_path="api")
)

@router.callback_query(lambda c:c.data in subscribes_list)
async def callback_subscribe(callback_query: CallbackQuery):
    subscribes_type = callback_query.data
    logger.debug("Logger Debug Sub Type %s",subscribes_type)
    subscribes_type_details = SUBSCRIBES_TYPE_DATA_REVERSE.get(subscribes_type)
    logger.debug("Logger Debug Sub Type %s",subscribes_type_details)
    data = None
    if subscribes_type_details is not None:
        async with get_async_db() as session:
            data = await subscribes_service.check_subscribes_user(user_id=callback_query.from_user.id,type_id=subscribes_type_details.get("type_id"),session=session)
    if data == True:
        await callback_query.message.edit_text(text=f"{subscribes_style_text.user_have_subscribe(description=subscribes_type_details.get("description",'-'))}",
                                               parse_mode=ParseMode.HTML,
                                               reply_markup=create_unsubscribes_keyboard(type_id=subscribes_type_details.get("type_id"),user_id = callback_query.from_user.id)
                                               )
    else:
        await callback_query.message.edit_text(text=f"{subscribes_style_text.user_dont_have_subscribe(description=subscribes_type_details.get("description",'-'))}",
                                               parse_mode=ParseMode.HTML,
                                               reply_markup=create_subscribes_keyboard(type_id=subscribes_type_details.get("type_id"),user_id = callback_query.from_user.id)
                                               )
    await callback_query.answer()

@router.callback_query(lambda c:c.data.startswith("subscribe_user"))
async def callback_subscribe_confirm(callback_query: CallbackQuery):
    subscribe_type_id,user_id=subscribe_correct(callback_query=callback_query,logger=logger)
    logger.debug("Logger Debug Sub Type %s",subscribe_type_id)
    if subscribe_type_id is None:
        return None
    async with get_async_db() as session:
        if await subscribes_service.subscribe(user_id=int(user_id),type_id=int(subscribe_type_id),session=session):
            await callback_query.message.edit_text(text=f"{subscribes_style_text.after_subscribes()}",parse_mode=ParseMode.HTML,reply_markup=inline_back_subscribe_menu)
        else:
            await callback_query.message.edit_text(text=f"{subscribes_style_text.after_bad_subscribe()}",parse_mode=ParseMode.HTML,reply_markup=inline_back_subscribe_menu)
    await callback_query.answer()

@router.callback_query(lambda c:c.data.startswith("unsubscribe_user"))
async def callback_unsubscribe_confirm(callback_query: CallbackQuery):
    subscribe_type_id,user_id=subscribe_correct(callback_query=callback_query,logger=logger)
    if subscribe_type_id is None:
        return None
    async with get_async_db() as session:
        if await subscribes_service.unsubscribe(user_id=callback_query.from_user.id,type_id=int(subscribe_type_id),session=session):
            await callback_query.message.edit_text(text=f"{subscribes_style_text.after_unsubscribe()}",parse_mode=ParseMode.HTML,reply_markup=inline_back_subscribe_menu)
        else:
            await callback_query.message.edit_text(text=f"{subscribes_style_text.after_bad_unsubscribe()}",parse_mode=ParseMode.HTML,reply_markup=inline_back_subscribe_menu)
    await callback_query.answer()

@router.callback_query(lambda c:c.data == "subscribe_main")
async def subscribe_main(callback_query: CallbackQuery):
    await callback_query.message.edit_text(text=f"{subscribes_message_menu}",parse_mode=ParseMode.MARKDOWN,reply_markup=await create_inline_subscribes_commands())