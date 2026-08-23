"""Bot buttons"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot import texts

CB_PRICE = "price"
CB_CARD = "card"
CB_BACK_PAYMENT = "back:payment"
CB_BACK_CONFIG = "back:config"


def config_menu() -> InlineKeyboardMarkup:
    """`/config` → `/price`"""
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.PRICE_PER_KM_BUTTON, callback_data=CB_PRICE)
    return builder.as_markup()


def price_menu() -> InlineKeyboardMarkup:
    """`/price` → Back → `/config`."""
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.BACK_BUTTON, callback_data=CB_BACK_CONFIG)
    return builder.as_markup()


def payment_menu() -> InlineKeyboardMarkup:
    """`/payment` → `/card`"""
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.CARD_BUTTON, callback_data=CB_CARD)
    return builder.as_markup()


def card_menu() -> InlineKeyboardMarkup:
    """`/card` → Back → `/payment`."""
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.BACK_BUTTON, callback_data=CB_BACK_PAYMENT)
    return builder.as_markup()
