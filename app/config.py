from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # MongoDB
    mongo_uri: SecretStr
    mongo_db: str = "ai"

    # OpenAI
    openai_key: SecretStr
    openai_base_url: str | None = None  # Provide base url to use Azure client
    azure_api_version: str = "2025-03-01-preview"
    client_timeout: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
