"""`/start` — root"""

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot import messages

router = Router(name="start")


@router.message(CommandStart())
async def show_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(messages.GREETING)
