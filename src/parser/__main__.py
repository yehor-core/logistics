"""Parser process entry point"""

import asyncio
import logging

from src.parser.client import RawPost, build_client, run_forever

logger = logging.getLogger(__name__)


async def _log_post(post: RawPost) -> None:
    logger.info("new post from %s (%s): %.80s", post.source, post.external_id, post.raw_text)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await run_forever(build_client(), _log_post)


if __name__ == "__main__":
    asyncio.run(main())
