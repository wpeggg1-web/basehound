"""
BASEHOUND Settings — loads from config/.env
"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


class Settings:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    BASESCAN_API_KEY: str = os.getenv("BASESCAN_API_KEY", "")
    GOPLUS_API_KEY: str = os.getenv("GOPLUS_API_KEY", "")

    # LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openrouter")   # openrouter | groq | pioneer
    LLM_MODEL: str = os.getenv("LLM_MODEL", "anthropic/claude-3-haiku")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1")

    # Interface
    INTERFACE: str = os.getenv("INTERFACE", "telegram")   # telegram | cli

    AGENT_NAME: str = os.getenv("AGENT_NAME", "BASEHOUND")


settings = Settings()
