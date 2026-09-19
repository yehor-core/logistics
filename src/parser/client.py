"""Telethon client that listens to configured source channels for new posts"""

import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from src.config import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RawPost:
    source_id: int
    external_id: int
    raw_text: str
    published_at: datetime


_PostHandler = Callable[[RawPost], Awaitable[None]]


def build_client() -> TelegramClient:
    return TelegramClient(
        settings.telegram_session_name,
        settings.telegram_api_id,
        settings.telegram_api_hash.get_secret_value(),
    )


def _to_raw_post(source_id: int, message: Message) -> RawPost | None:
    if not message.raw_text or not message.date:
        return None
    return RawPost(
        source_id=source_id,
        external_id=message.id,
        raw_text=message.raw_text,
        published_at=message.date,
    )


def register_handlers(
    client: TelegramClient,
    source_channels: list[int],
    on_post: _PostHandler,
) -> None:
    @client.on(events.NewMessage(chats=source_channels))
    async def _handler(event: events.NewMessage.Event) -> None:
        post = _to_raw_post(event.chat_id, event.message)
        if post is not None:
            await on_post(post)


async def run_forever(
    client: TelegramClient,
    source_channels: list[int],
    on_post: _PostHandler,
) -> None:
    register_handlers(client, source_channels, on_post)
    # Note: Advanced error handling (AuthKeyUnregisteredError,
    # FloodWaitError affecting Sources.is_enabled) deferred per docs/08-errors.md
    await client.start()
    logger.info(
        "parser connected, listening on %d channels",
        len(source_channels),
    )
    await client.run_until_disconnected()
