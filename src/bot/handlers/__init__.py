"""Routers for every command"""

from aiogram import Router

from src.bot.handlers import card, config, on_off, payment, price, start

routers: tuple[Router, ...] = (
    start.router,
    on_off.router,
    config.router,
    price.router,
    payment.router,
    card.router,
)

__all__ = ["routers"]
