"""Bot entry point"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from src.bot.handlers import routers
from src.config import settings

BOT_COMMANDS = [
    BotCommand(command="start", description="Начать работу"),
    BotCommand(command="on_off", description="Включить / выключить уведомления"),
    BotCommand(command="config", description="Настройки"),
    # BotCommand(command="source", description="Источники данных"), TODO: uncomment after db launch
    BotCommand(command="payment", description="Оплата подписки"),
]


def build_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_routers(*routers)

    return dispatcher


async def main() -> None:
    bot = Bot(token=settings.test_bot_token.get_secret_value())
    dispatcher = build_dispatcher()

    await bot.set_my_commands(BOT_COMMANDS)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
