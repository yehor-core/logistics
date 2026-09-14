"""Project entry point."""

import asyncio

from src.bot.__main__ import main as run_bot


def main() -> None:
    asyncio.run(run_bot())
