import aiohttp
from aiogram import types

from bot.utils.database.postgres import DataBase


async def cmd_get_comments(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/comments') as resp:
            responce = await resp.json()
            for comment in responce:
                await DataBase.execute(
                    "INSERT INTO comments(name, email, body) VALUES($1, $2, $3)",
                    comment['name'],
                    comment['email'],
                    comment['body'],
                    execute=True
                )
            else:
                await message.answer(
                    "Данные о пользователях и их комментариях успешно загружены в базу данных."
                )
