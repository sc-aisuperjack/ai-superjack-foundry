from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    app_name: str = "Agentic Foundry"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    mongodb_uri: str = "mongodb://localhost:27020"
    mongodb_db_name: str = "agentic_foundry"
    redis_url: str = "redis://localhost:6380/0"
    default_llm_provider: str = "mock"
    enable_mocks: bool = True

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_chat_model: str = Field(default="gpt-4o-mini", alias="OPENAI_CHAT_MODEL")
    openai_stt_model: str = Field(default="gpt-4o-mini-transcribe", alias="OPENAI_STT_MODEL")
    openai_tts_model: str = Field(default="gpt-4o-mini-tts", alias="OPENAI_TTS_MODEL")
    openai_tts_voice: str = Field(default="alloy", alias="OPENAI_TTS_VOICE")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
