"""Entry point for the parser component: `python -m app.parser`.

Connects the Telethon client -- prompting interactively for a phone number
and login code the very first time, when no `.session` file exists yet at
`settings.telegram_session_path` -- registers the new-message listener on
the configured test channel, and blocks until disconnected (Ctrl+C to stop).

Deliberately out of scope here (see docs/08-errors.md #1 and the approved
plan for this task): writing to Posts/Sources, retry/alerting beyond
Telethon's own defaults (e.g. its `flood_sleep_threshold`), and
multi-channel support driven by the `Sources` table.
"""

import asyncio

from app.config import settings
from app.parser.client import build_client, register_handlers


async def main() -> None:
    client = build_client()
    await client.start()
    register_handlers(client, settings.telegram_test_channel)
    print(
        f"Connected. Listening for new messages on "
        f"{settings.telegram_test_channel} (Ctrl+C to stop)."
    )
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
