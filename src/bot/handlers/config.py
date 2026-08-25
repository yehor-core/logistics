"""`/config` — settings menu"""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot import messages
from src.bot.keyboards import CB_BACK_CONFIG, config_menu

router = Router(name="config")


@router.message(Command("config"))
async def show_config(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(messages.CONFIG, reply_markup=config_menu())


@router.callback_query(F.data == CB_BACK_CONFIG)
async def back_to_config(callback: CallbackQuery, state: FSMContext) -> None:
    """Back → `/config` from `/price`; also leaves the price-input state."""
    await state.clear()
    await callback.answer()
    if isinstance(callback.message, Message):
        await callback.message.edit_text(messages.CONFIG, reply_markup=config_menu())
