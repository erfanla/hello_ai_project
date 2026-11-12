"""All app settings, in one place.

Every value comes from an environment variable (or a `.env` file).
For example, `DATABASE_URL=sqlite:///./other.db` changes `settings.database_url`.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./app.db"
    app_env: str = "dev"


settings = Settings()
