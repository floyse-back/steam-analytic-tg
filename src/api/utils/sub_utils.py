from aiogram.types import CallbackQuery

from src.domain.logger import ILogger


def subscribe_correct(callback_query: CallbackQuery,logger:ILogger):
    callback_split_data = callback_query.data.split(":")
    logger.debug("callback_split_data: %s",callback_split_data)
    subscribe_type_id = callback_split_data[1]
    user_id = callback_split_data[2]
    logger.debug("user_id: %s vs callback_query.from_user.id = %s",user_id,callback_query.from_user.id)
    if int(user_id) != callback_query.from_user.id:
        return None,None
    return subscribe_type_id,user_id