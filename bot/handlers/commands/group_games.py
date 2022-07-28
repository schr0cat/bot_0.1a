from aiogram import types

from bot.filters.chat_type import ChatTypeFilter


# message(ChatTypeFilter(chat_type=['group', 'supergroup'])
async def cmd_casino_in_group(message: types.Message):
    await message.answer_dice(emoji="🎰")


async def cmd_basketball_in_group(message: types.Message):
    await message.answer_dice(emoji="🏀")
