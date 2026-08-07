"""Telethon (MTProto) client for the parser component.

Scope for this task (see docs/02-architecture.md's "Parser" component and
the approved plan): establish a connection using a persisted Telethon
.session file and print the raw text of new messages from a single
configured test channel. No DB writes, no `Sources`-table lookup, no
price/route parsing yet -- those land in a follow-up task, per
docs/06-matching.md.

`build_client()` reads `app.config.settings` lazily (inside the function
body, not at module import time) so this module -- and in particular the
pure `extract_text` helper -- stays importable in tests even before real
TELEGRAM_API_ID / TELEGRAM_API_HASH / TELEGRAM_TEST_CHANNEL values exist
in `.env`.
"""

from telethon import TelegramClient, events


def build_client() -> TelegramClient:
    """Construct a Telethon client from app settings.

    Deliberately does not connect or log in -- call `await client.start()`
    separately (see `app/parser/__main__.py`).
    """
    from app.config import settings  # deferred: see module docstring

    return TelegramClient(
        settings.telegram_session_path,
        settings.telegram_api_id,
        settings.telegram_api_hash,
    )


def extract_text(event) -> str | None:
    """Pull the raw text out of a Telethon NewMessage event.

    Returns None for a missing, empty, or whitespace-only `raw_text` (e.g.
    photos, stickers, or other non-text messages) so callers can skip those
    without extra checks.
    """
    text = getattr(event, "raw_text", None)
    if text is None:
        return None
    text = text.strip()
    return text or None


def register_handlers(client: TelegramClient, chat: str) -> None:
    """Attach a new-message listener for `chat` that prints extracted text.

    `chat` is whatever's configured in TELEGRAM_TEST_CHANNEL: a @username
    or a numeric chat id such as "-1001234567890". Numeric-looking strings
    are coerced to int, since Telethon expects numeric peer ids as ints,
    not numeric strings.
    """
    target: str | int = int(chat) if chat.lstrip("-").isdigit() else chat

    async def _on_new_message(event: events.NewMessage.Event) -> None:
        text = extract_text(event)
        if text is None:
            return
        print(f"[chat={event.chat_id} msg={event.id}] {text}")

    client.add_event_handler(_on_new_message, events.NewMessage(chats=target))
