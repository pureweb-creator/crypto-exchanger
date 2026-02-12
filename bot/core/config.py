from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL: str = "sqlite+aiosqlite:///./db.sqlite3"
    DEBUG: bool = False
    SUPPORT_URL: str | None = None
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: SecretStr
    REDIS_USER: str | None = None
    REDIS_USER_PASSWORD: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
