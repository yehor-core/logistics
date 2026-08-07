"""Application-wide environment settings.

Per CLAUDE.md: "Secrets via env only ... All env reading goes through
app/config.py." This currently only holds settings for the Telegram MTProto
parser (PR1 of the parser bootstrap, see docs/02-architecture.md and
docs/09-code-structure.md). Later work (bot, DB, payments, ...) should add
its fields to this same `Settings` class rather than reading `os.environ`
directly elsewhere.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Telegram MTProto parser (Telethon) ---
    # api_id / api_hash: issued per-application at https://my.telegram.org
    telegram_api_id: int
    telegram_api_hash: str
    # Path to the Telethon .session file. Telethon appends the .session
    # extension itself, so this should be a path *without* it, e.g.
    # "./sessions/parser" -> "./sessions/parser.session".
    telegram_session_path: str = "./sessions/parser"
    # Single test channel to listen on for now: @username or a numeric
    # chat id (e.g. -1001234567890). Not sourced from the `Sources` table
    # yet -- see docs/02-architecture.md for the eventual multi-source design.
    telegram_test_channel: str


settings = Settings()
