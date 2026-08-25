"""`/price` — price per km setting"""

import math

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message

from src.bot import messages
from src.bot.keyboards import CB_PRICE, price_menu
from src.config import settings

router = Router(name="price")

waiting_for_price = State("waiting_for_price")


def _format_price(price: float) -> str:
    return f"{price:g}"


def _parse_price(raw_price: str | None) -> float | None:
    if raw_price is None:
        return None
    try:
        price = float(raw_price.strip().replace(",", "."))
    except ValueError:
        return None
    if not math.isfinite(price) or price < 0:
        return None
    return price


@router.callback_query(F.data == CB_PRICE)
async def ask_price(callback: CallbackQuery, state: FSMContext) -> None:
    # TODO: read user's price per km, after creating a db
    current_price = settings.default_price_per_km

    await state.set_state(waiting_for_price)
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            messages.PRICE_PER_KM.format(current_price=_format_price(current_price)),
            reply_markup=price_menu(),
        )


@router.message(waiting_for_price)
async def set_price(message: Message, state: FSMContext) -> None:
    new_price = _parse_price(message.text)
    if new_price is None:
        await message.answer(messages.PRICE_INVALID)
        return

    # TODO(repositories/users.py): persist new_price on `User settings.price_per_km`.
    await state.clear()
    await message.answer(messages.PRICE_UPDATED.format(new_price=_format_price(new_price)))
