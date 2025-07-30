from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def message_delete(message: Message, state: FSMContext):
    data = await state.get_data()
    if data.get("message_id") and data.get("chat_id"):
        await message.bot.delete_message(message_id=data.get("message_id"), chat_id=data.get("chat_id"))
    await state.clear()