from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    SUPPORT_URL: str | None = None

    POSTGRES_DB_URL: str = "postgres+asyncpg://user:pass@localhost:5432/dbname"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: SecretStr
    REDIS_USER: str
    REDIS_USER_PASSWORD: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
