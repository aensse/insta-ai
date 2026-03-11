from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    app_name: str = "insta-ai"
    db_name: str = "insta-ai.db"

    username: str
    password: str
    secret: str | None = None

    ai_instructions_file: Path = Field(default=Path(__file__).parent.parent.parent/"instructions.txt")
    ig_session_file: Path = Field(default=Path(__file__).parent.parent.parent/"ig_session.json")

    llm_api_key: SecretStr
    llm_model: str = "grok-4-1-fast-non-reasoning"

    @property
    def db_url(self):
        return f"sqlite+aiosqlite:///./{self.db_name}"


settings = Settings()

