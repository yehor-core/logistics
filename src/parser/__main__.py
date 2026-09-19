import asyncio
import logging
import sys

from sqlalchemy import select

from src.db.session import async_session_maker
from src.db.models import Source
from src.parser.client import build_client, run_forever, RawPost

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def on_post(post: RawPost) -> None:
    logger.info("New post from source %s: %s...", post.source_id, post.raw_text[:50].replace('\n', ' '))


async def main() -> None:
    logger.info("Fetching source channels from database...")
    
    async with async_session_maker() as session:
        # Строго по docs/03-data-model.md: используем chat_id, а не telegram_id
        result = await session.execute(select(Source.chat_id))
        channels = list(result.scalars().all())

    if not channels:
        logger.warning("No source channels found in database. Exiting.")
        return

    client = build_client()
    await run_forever(client, source_channels=channels, on_post=on_post)


if __name__ == "__main__":
    asyncio.run(main())
    