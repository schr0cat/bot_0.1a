from random import randint

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="click on me",
        callback_data="random_value")
    )
    await message.answer(
        "Click on button and bot return a number from 1 to 10",
        reply_markup=builder.as_markup()
    )


async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer()
