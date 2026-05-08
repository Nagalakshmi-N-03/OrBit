from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "OrBit"
    APP_ENV: str = "development"
    APP_PORT: int = 8000

    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None

    DATABASE_URL: str = "sqlite:///./orbit.db"
    FRONTEND_URL: str = "http://localhost:3000"

    MAX_RETRIES: int = 3
    CONFIDENCE_THRESHOLD: float = 0.7
    DEFAULT_MODE: str = "balanced"

    PRIMARY_MODEL: str = "gpt-4o-mini"
    FALLBACK_MODEL: str = "gpt-4o"
    MAX_TOKENS: int = 4096
    TEMPERATURE_FAST: float = 0.3
    TEMPERATURE_BALANCED: float = 0.2
    TEMPERATURE_QUALITY: float = 0.1

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()