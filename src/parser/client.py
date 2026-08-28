"""Telethon client that listens to configured source channels for new posts"""

import asyncio
import logging
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from telethon import TelegramClient, events
from telethon.errors import AuthKeyUnregisteredError, FloodWaitError
from telethon.tl.custom.message import Message
from src.config import settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RawPost:
    source: int
    external_id: int
    raw_text: str
    published_at: datetime


PostHandler = Callable[[RawPost], Awaitable[None]]


def build_client() -> TelegramClient:
    return TelegramClient(
        settings.telegram_session_name,
        settings.telegram_api_id,
        settings.telegram_api_hash.get_secret_value(),
    )


def _to_raw_post(source: int, message: Message) -> RawPost | None:
    if not message.raw_text:
        return None
    return RawPost(
        source=source,
        external_id=message.id,
        raw_text=message.raw_text,
        published_at=message.date or datetime.now(UTC),
    )


def register_handlers(client: TelegramClient, on_post: PostHandler) -> None:
    @client.on(events.NewMessage(chats=settings.source_channels))
    async def _handler(event: events.NewMessage.Event) -> None:
        post = _to_raw_post(event.chat_id, event.message)
        if post is not None:
            await on_post(post)


async def run_forever(client: TelegramClient, on_post: PostHandler) -> None:
    register_handlers(client, on_post)
    while True:
        try:
            await client.start()
            logger.info("parser connected, listening on %d channels", len(settings.source_channels))
            await client.run_until_disconnected()
            return
        except FloodWaitError as exc:
            logger.warning("flood wait, retrying in %ss", exc.seconds)
            await asyncio.sleep(exc.seconds)
        except AuthKeyUnregisteredError:
            logger.critical("telegram session revoked, re-authentication required")
            raise
