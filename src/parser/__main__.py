"""Parser process entry point"""

import asyncio
import logging

from src.parser.client import RawPost, build_client, run_forever

logger = logging.getLogger(__name__)


async def _log_post(post: RawPost) -> None:
    # TODO: remove after DB persistence lands
    logger.info("new post from source %s", post.source_id)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    await run_forever(build_client(), _log_post)


if __name__ == "__main__":
    asyncio.run(main())
