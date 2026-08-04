import asyncio
from aiogram import Bot

async def notification_worker(bot: Bot, db_pool):
    while True:
        await asyncio.sleep(60)
        
        async with db_pool.acquire() as conn:
            users = await conn.fetch(
                "SELECT user_id, notif_routes, notif_status FROM user_settings WHERE is_enabled = true"
            )
            
            for row in users:
                user_id = row['user_id']
                
                if row['notif_routes']:
                    try:
                        await bot.send_message(user_id, "🔔 [Тест] Найден новый выгодный маршрут!")
                    except Exception:
                        pass
                        
                if row['notif_status']:
                    try:
                        await bot.send_message(user_id, "📩 [Тест] Статус вашего груза изменился.")
                    except Exception:
                        pass