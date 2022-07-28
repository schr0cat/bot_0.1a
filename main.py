import asyncio


from aiogram import Router, Bot, Dispatcher
from aiogram.types import BotCommand

from bot.handlers.commands import commands_register
from bot.handlers.commands.user import register_states_handler
from bot.utils.config_reader import config
from bot.utils.database.postgres import DataBase
from bot.utils.logger import logger


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description="Зарегистрироваться в боте"),
        BotCommand(command='new_user', description="Добавить нового пользователя"),
        BotCommand(command='cancel', description="Отменить текущее действие"),
        BotCommand(command='random', description="Вывести рандомное число"),
        BotCommand(command='basketball', description="Бросить мяч в корзину"),
        BotCommand(command='casino', description="Сыграть в игровой автомат")
    ]
    await bot.set_my_commands(commands)


async def start_up():
    default_router = Router()
    # Создаем экземпляр бота, передаем токен, устанавливаем мод кодировки.
    bot = Bot(token=config.token, parse_mode="HTML")
    # Создаем экземпляр диспетчера бота.
    dp = Dispatcher()
    # Привязываем к нему роутер.
    dp.include_router(default_router)

    logger.info("Запуск бота.")
    commands_register(default_router)
    register_states_handler(default_router)

    await set_bot_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), config=config)


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(DataBase.create_pool())
        loop.run_until_complete(start_up())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот остановлен !")
