"""`/card` — hands the user a Monobank invoice link"""

# TODO: this file is currently a mock. we should refactor this at the end of the MVP
# with the full payment proccess

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.bot import messages
from src.bot.keyboards import CB_CARD, card_menu

router = Router(name="card")

_PLACEHOLDER_PAYMENT_LINK = "https://pay.mbnk.biz/"


@router.callback_query(F.data == CB_CARD)
async def show_card(callback: CallbackQuery) -> None:
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(
            messages.CARD.format(payment_link=_PLACEHOLDER_PAYMENT_LINK),
            reply_markup=card_menu(),
        )
