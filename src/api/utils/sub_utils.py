from aiogram.types import CallbackQuery


def subscribe_correct(callback_query: CallbackQuery):
    callback_split_data = callback_query.data.split(":")
    subscribe_type_id = callback_split_data[1]
    user_id = callback_split_data[2]
    if user_id != callback_query.from_user.id:
        return None,None
    return subscribe_type_id,user_id