"""Environment settings"""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables from .env"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    test_bot_token: SecretStr = Field(alias="TEST_BOT")
    test_bot_handle: str = Field(alias="TEST_BOT_HANDLE")
    default_price_per_km: float = Field(default=65, alias="DEFAULT_PRICE_PER_KM")

    telegram_api_id: int = Field(alias="TELEGRAM_API_ID")
    telegram_api_hash: SecretStr = Field(alias="TELEGRAM_API_HASH")
    telegram_session_name: str = Field(default="parser", alias="TELEGRAM_SESSION_NAME")
    source_channels_raw: str = Field(alias="SOURCE_CHANNELS")

    @property
    def source_channels(self) -> list[str | int]:
        channels: list[str | int] = []
        for raw in self.source_channels_raw.split(","):
            chat = raw.strip()
            if not chat:
                continue
            channels.append(int(chat) if chat.lstrip("-").isdigit() else chat)
        return channels


settings = Settings()
