from aiogram import Bot, Dispatcher
from aiogram.client.bot import BotCommand, BotCommandScopeDefault
import asyncio
import os
import logging

from routers.user_router import router as user_router

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))  # указываем токен бота

commands = [
    BotCommand(command='/reg', description='Регистрация пользователя'),
    BotCommand(command='/add_operation', description='Добавление операции'),
    BotCommand(command='/operations', description='Просмотр всех операций')
]  # список команд бота


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher()
    dp.include_router(user_router)  # подключаем роутер
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())  # устанавливаем команды
    await dp.start_polling(bot)  # запускаем бота


if __name__ == '__main__':
    asyncio.run(main())
