from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # MongoDB
    mongo_uri: SecretStr
    mongo_db: str = "ai"

    # OpenAI
    openai_key: SecretStr

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


config = Config()
