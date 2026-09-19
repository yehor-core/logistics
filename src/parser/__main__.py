import asyncio
import logging
import sys

from sqlalchemy import select

from src.db.models import Post, Source
from src.db.session import session_factory
from src.enums import PostStatus
from src.parser.client import RawPost, build_client, run_forever

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    logger.info("Fetching active source channels from database...")

    async with session_factory() as session:
        result = await session.execute(select(Source.id, Source.chat_id).where(Source.is_enabled))
        chat_id_to_source_id = {
            chat_id: source_id for source_id, chat_id in result.all() if chat_id is not None
        }

    if not chat_id_to_source_id:
        logger.warning("No active source channels found in database. Exiting.")
        return

    async def on_post(post: RawPost) -> None:
        source_id = chat_id_to_source_id.get(post.chat_id)
        if source_id is None:
            return

        txt = post.raw_text[:50].replace("\n", " ")
        logger.info("New post from source %s: %s...", source_id, txt)

        async with session_factory() as session:
            session.add(
                Post(
                    source_id=source_id,
                    external_id=post.external_id,
                    raw_text=post.raw_text,
                    published_at=post.published_at,
                    status=PostStatus.NEW,
                )
            )
            await session.commit()

    client = build_client()
    await run_forever(client, source_channels=list(chat_id_to_source_id), on_post=on_post)


if __name__ == "__main__":
    asyncio.run(main())
