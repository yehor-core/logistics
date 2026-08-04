from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
import aiohttp
import os

router = Router()

class ConfigState(StatesGroup):
    waiting_for_price = State()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = [
        [KeyboardButton(text="Вкл/Выкл"), KeyboardButton(text="Настройки")],
        [KeyboardButton(text="Источники"), KeyboardButton(text="Оплата")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    text = (
        "Привет! Я бот логист.\n"
        "Помогаю автоматизировать работу.\n"
        "Выберите раздел ниже, чтобы начать"
    )
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text == "Вкл/Выкл")
async def btn_on_off(message: types.Message, db_pool):
    user_id = message.from_user.id
    
    async with db_pool.acquire() as conn:
        current_status = await conn.fetchval(
            "SELECT is_enabled FROM user_settings WHERE user_id = $1", user_id
        )
        
        if current_status is None:
            await conn.execute(
                "INSERT INTO user_settings (user_id, is_enabled, price_per_km) VALUES ($1, $2, $3)",
                user_id, True, 25.0
            )
            new_status = True
        else:
            new_status = not current_status
            await conn.execute(
                "UPDATE user_settings SET is_enabled = $1 WHERE user_id = $2",
                new_status, user_id
            )

    if new_status:
        text = "☑ Запущено\nБот начал работу и будет присылать уведомления согласно вашим настройкам."
    else:
        text = "☐ Остановлено\nБот приостановлен. Уведомления приходить не будут, пока вы не включите его снова."
        
    await message.answer(text)

@router.message(F.text == "Настройки")
async def btn_config(message: types.Message):
    kb = [
        [InlineKeyboardButton(text="Цена за км", callback_data="price")],
        [InlineKeyboardButton(text="Уведомления", callback_data="notifications")],
        [InlineKeyboardButton(text="Назад", callback_data="delete_msg")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    text = (
        "⚙️ Настройки\n"
        "Здесь можно изменить параметры работы бота:\n"
        "Цена за км — влияет на расчёт стоимости поездки/заказа\n"
        "Уведомления — включить/выключить конкретные типы оповещений\n"
        "Выберите пункт, который хотите изменить"
    )
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text == "Источники")
async def btn_sources(message: types.Message, db_pool):
    user_id = message.from_user.id
    kb = []
    
    async with db_pool.acquire() as conn:
        sources = await conn.fetch("""
            SELECT s.id, s.name, us.is_enabled 
            FROM sources s
            LEFT JOIN user_sources us ON s.id = us.source_id AND us.user_id = $1
            WHERE s.is_enabled = true
        """, user_id)
        
        for src in sources:
            is_on = src['is_enabled'] if src['is_enabled'] is not None else False
            icon = "☑" if is_on else "☐"
            kb.append([InlineKeyboardButton(text=f"{icon} {src['name']}", callback_data=f"src_{src['id']}")])
            
    kb.append([InlineKeyboardButton(text="Назад", callback_data="delete_msg")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    text = "☑ Источники данных\nВыберите, какие источники использовать."
    await message.answer(text, reply_markup=keyboard)

@router.message(F.text == "Оплата")
async def btn_payment(message: types.Message):
    kb = [
        [InlineKeyboardButton(text="Оплатить картой", callback_data="card")],
        [InlineKeyboardButton(text="Назад", callback_data="delete_msg")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    text = "💳 Оплата\nДоступные варианты оплаты: Банковская карта (Visa/Mastercard)\nСтоимость подписки: 500 ₴/месяц"
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("src_"))
async def toggle_source(callback: CallbackQuery, db_pool):
    user_id = callback.from_user.id
    source_id = int(callback.data.split("_")[1])
    
    async with db_pool.acquire() as conn:
        current = await conn.fetchval(
            "SELECT is_enabled FROM user_sources WHERE user_id = $1 AND source_id = $2",
            user_id, source_id
        )
        
        if current is None:
            await conn.execute(
                "INSERT INTO user_sources (user_id, source_id, is_enabled) VALUES ($1, $2, $3)",
                user_id, source_id, True
            )
        else:
            await conn.execute(
                "UPDATE user_sources SET is_enabled = $1 WHERE user_id = $2 AND source_id = $3",
                not current, user_id, source_id
            )
            
    await btn_sources(callback.message, db_pool)
    await callback.answer("Статус источника изменен!")

@router.callback_query(F.data == "price")
async def process_price_btn(callback: CallbackQuery, state: FSMContext, db_pool):
    user_id = callback.from_user.id
    async with db_pool.acquire() as conn:
        price = await conn.fetchval("SELECT price_per_km FROM user_settings WHERE user_id = $1", user_id)
        current_price = price if price is not None else 25.0

    text = f"Укажите цену за 1 км\nОтправьте число (например: 25 или 25.5).\nТекущее значение: {current_price} ₴/км"
    await callback.message.edit_text(text)
    await state.set_state(ConfigState.waiting_for_price)
    await callback.answer()

@router.message(ConfigState.waiting_for_price)
async def process_price_input(message: types.Message, state: FSMContext, db_pool):
    user_id = message.from_user.id
    kb = [[InlineKeyboardButton(text="Назад к настройкам", callback_data="back_to_config")]]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    try:
        new_price = float(message.text.replace(',', '.'))
        async with db_pool.acquire() as conn:
            await conn.execute(
                "UPDATE user_settings SET price_per_km = $1 WHERE user_id = $2",
                new_price, user_id
            )
        text = f"☑ Цена обновлена: {new_price} ₴/км\nИзменения вступили в силу."
        await state.clear()
    except ValueError:
        text = "☑ Не удалось распознать число. Пожалуйста, отправьте цену цифрами, например: 30"
    
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "back_to_config")
async def back_to_config(callback: CallbackQuery):
    await callback.message.delete()
    await btn_config(callback.message)
    await callback.answer()

@router.callback_query(F.data == "card")
async def process_card_btn(callback: CallbackQuery, db_pool):
    user_id = callback.from_user.id
    amount = 500
    mono_token = os.getenv("MONOBANK_TOKEN")
    
    if not mono_token:
        payment_link = "https://monobank.ua/"
        invoice_id = "test_invoice_123"
    else:
        url = "https://api.monobank.ua/api/merchant/invoice/create"
        headers = {"X-Token": mono_token}
        payload = {
            "amount": amount * 100,
            "ccy": 980,
            "redirectUrl": "https://t.me/",
            "webHookUrl": "https://example.com/webhook"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    payment_link = data.get("pageUrl")
                    invoice_id = data.get("invoiceId")
                else:
                    await callback.answer("Ошибка создания платежа в Monobank", show_alert=True)
                    return

    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO payments (user_id, method_id, amount, status, external_id, created_at)
            VALUES ($1, 'monobank', $2, 'pending', $3, NOW())
        """, user_id, amount, invoice_id)

    kb = [
        [InlineKeyboardButton(text="Оплатить по ссылке", url=payment_link)],
        [InlineKeyboardButton(text="Назад", callback_data="delete_msg")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    
    text = (
        "💳 Оплата через Monobank\n"
        f"Сумма к оплате: {amount} ₴\n\n"
        "Нажмите кнопку ниже для перехода на защищенную страницу оплаты:"
    )
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "delete_msg")
async def delete_inline_msg(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data == "notifications")
async def notifications_menu(callback: CallbackQuery, db_pool):
    user_id = callback.from_user.id
    
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT notif_routes, notif_status FROM user_settings WHERE user_id = $1",
            user_id
        )
        
        if not row:
            await conn.execute(
                "INSERT INTO user_settings (user_id, notif_routes, notif_status) VALUES ($1, $2, $3)",
                user_id, True, True
            )
            routes_val, status_val = True, True
        else:
            routes_val = row['notif_routes'] if row['notif_routes'] is not None else True
            status_val = row['notif_status'] if row['notif_status'] is not None else True

    kb = [
        [InlineKeyboardButton(text=f"🔔 Новые маршруты: {'✅' if routes_val else '✔️'}", callback_data="tgl_routes")],
        [InlineKeyboardButton(text=f"📩 Изменения статуса: {'✅' if status_val else '✔️'}", callback_data="tgl_status")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_config")]
    ]
    
    try:
        await callback.message.edit_text(
            "⚙️ Точечная настройка уведомлений\nВыберите типы оповещений:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
        )
    except TelegramBadRequest:
        pass
        
    await callback.answer()

@router.callback_query(F.data.startswith("tgl_"))
async def toggle_specific_notification(callback: CallbackQuery, db_pool):
    user_id = callback.from_user.id
    action = callback.data.replace("tgl_", "")
    
    allowed_columns = {
        "routes": "notif_routes",
        "status": "notif_status"
    }
    
    if action not in allowed_columns:
        await callback.answer("Ошибка", show_alert=True)
        return
        
    column = allowed_columns[action]
    
    async with db_pool.acquire() as conn:
        current_val = await conn.fetchval(
            f"SELECT {column} FROM user_settings WHERE user_id = $1", 
            user_id
        )
        new_val = not bool(current_val)
        
        await conn.execute(
            f"UPDATE user_settings SET {column} = $1 WHERE user_id = $2",
            new_val, user_id
        )
        
    await notifications_menu(callback, db_pool)