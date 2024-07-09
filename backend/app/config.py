import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    APP_NAME: str = os.getenv("APP_NAME", "shortURL")
    APP_PROTOCOL: str = os.getenv("APP_PROTOCOL", "http")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = os.getenv("APP_PORT", 8000)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "0.0.0.0")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6378)
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "x326y457z")
    MINI_URL: str = os.getenv("MINI_URL", f"{APP_PROTOCOL}://{APP_HOST}:{APP_PORT}/")
    REDIS_URL: str = os.getenv("REDIS_URL", f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0")


settings = Settings()
