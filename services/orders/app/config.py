from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://orders_user:orders_pass@orders-db:5432/orders_db"
    JWT_SECRET: str = "super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    REDIS_URL: str = "redis://redis:6379/0"
    ANTHROPIC_API_KEY: Optional[str] = None
    CACHE_TTL: int = 60  # seconds

    class Config:
        env_file = ".env"

settings = Settings()
