from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # MongoDB
    mongo_uri: SecretStr
    mongo_db: str = "ai"

    # OpenAI
    openai_key: SecretStr
    openai_base_url: str
    azure_api_version: str = "2025-02-01-preview"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
