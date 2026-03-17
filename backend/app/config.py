from functools import lru_cache
import os


class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://english_user:english_password@localhost:5432/english_growth",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
