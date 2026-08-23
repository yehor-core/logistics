"""Environment settings"""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables from .env"""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    test_bot_token: SecretStr = Field(alias="TEST_BOT")
    test_bot_handle: str = Field(alias="TEST_BOT_HANDLE")


settings = Settings()
