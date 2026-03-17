from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    default_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")


    @property
    def cors_allow_origins(self) -> list[str]:
        origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
        return [origin.strip() for origin in origins.split(",") if origin.strip()]

    @property
    def database_url(self) -> str:
        if self.app_env.lower() == "development":
            default_sqlite_path = Path(__file__).resolve().parents[2] / "data" / "english_growth.db"
            default_sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            return os.getenv("DATABASE_URL", f"sqlite:///{default_sqlite_path}")

        return os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg://english_user:english_password@localhost:5432/english_growth",
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
