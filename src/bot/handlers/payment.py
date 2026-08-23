"""`/payment` — subscription payment menu"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot import messages
from src.bot.keyboards import CB_BACK_PAYMENT, payment_menu

router = Router(name="payment")

# TODO(repositories/subscriptions.py): the plan (price, duration) comes from `Features`.
# Hardcoded until that table exists.
_PLACEHOLDER_PRICE = 0
_PLACEHOLDER_PERIOD = "мес"


def _payment_text() -> str:
    return messages.PAYMENT.format(price=_PLACEHOLDER_PRICE, period=_PLACEHOLDER_PERIOD)


@router.message(Command("payment"))
async def show_payment(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_payment_text(), reply_markup=payment_menu())


@router.callback_query(F.data == CB_BACK_PAYMENT)
async def back_to_payment(callback: CallbackQuery) -> None:
    """Back → `/payment` from `/card`."""
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(_payment_text(), reply_markup=payment_menu())
