"""`/on_off`"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot import messages

router = Router(name="on_off")

# TODO(repositories/users.py): replace with `User settings.is_enabled`. In-memory state
# is per-process and lost on restart — placeholder until the DB layer lands.
_is_enabled: dict[int, bool] = {}


@router.message(Command("on_off"))
async def toggle(message: Message) -> None:
    # TODO: this part of code feels like AI slop. i will refactor it later
    is_enabled = not _is_enabled.get(message.from_user.id, False)
    _is_enabled[message.from_user.id] = is_enabled
    await message.answer(messages.ON if is_enabled else messages.OFF)
