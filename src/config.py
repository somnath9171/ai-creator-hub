import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:supersecure_db_password_2026@postgres:5432/aicreatorhub"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecure_secret_fallback_key_2026")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
