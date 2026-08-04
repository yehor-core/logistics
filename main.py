import asyncio
import os
from pathlib import Path
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router
from db import create_pool
from worker import notification_worker

async def main():
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    
    db_pool = await create_pool()
    dp["db_pool"] = db_pool
    
    dp.include_router(router)
    
    asyncio.create_task(notification_worker(bot, db_pool))
    
    print("Бот успешно запущен и подключен к базе!")
    await dp.start_polling(bot, db_pool=db_pool)

if __name__ == "__main__":
    asyncio.run(main())