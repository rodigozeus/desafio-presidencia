from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://users_user:users_pass@users-db:5432/users_db"
    JWT_SECRET: str = "super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"

settings = Settings()
