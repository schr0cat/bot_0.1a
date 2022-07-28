import aiohttp
from aiogram import types

from bot.utils.database.postgres import DataBase


async def cmd_get_users(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://jsonplaceholder.typicode.com/posts') as resp:
            responce = await resp.json()
            for user in responce:
                await DataBase.execute(
                    "INSERT INTO new_users("
                    "title, body)"
                    " VALUES($1, $2)",
                    user['title'],
                    user['body'],
                    execute=True
                )
            else:
                await message.answer("Все данные пользователей отправлены в базу данных.")
