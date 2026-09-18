"""Environment defaults so src.config imports without a local .env"""

import os

os.environ.setdefault("TEST_BOT", "0:test")
os.environ.setdefault("TEST_BOT_HANDLE", "@test_bot")
os.environ["DATABASE_URL"] = "postgresql+asyncpg://logistics:test@postgres:5432/logistics"
