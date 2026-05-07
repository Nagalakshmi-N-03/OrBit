from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "OrBit"
    APP_ENV: str = "development"
    APP_PORT: int = 8000
    
    # API Keys
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str = "sqlite:///./orbit.db"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Pipeline Settings
    MAX_RETRIES: int = 3
    CONFIDENCE_THRESHOLD: float = 0.7
    DEFAULT_MODE: str = "balanced"  # fast / balanced / quality
    
    # LLM Settings
    PRIMARY_MODEL: str = "claude-sonnet-4-20250514"
    FALLBACK_MODEL: str = "gpt-4o"
    MAX_TOKENS: int = 4096
    TEMPERATURE_FAST: float = 0.3
    TEMPERATURE_BALANCED: float = 0.2
    TEMPERATURE_QUALITY: float = 0.1

    class Config:
        env_file = ".env"
        extra = "allow"

# Single instance used everywhere
settings = Settings()