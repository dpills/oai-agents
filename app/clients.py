from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from openai import AsyncAzureOpenAI

from .config import config

db: AsyncIOMotorDatabase[Any] = AsyncIOMotorClient(config.mongo_uri.get_secret_value())[
    config.mongo_db
]

openai_client = AsyncAzureOpenAI(
    api_key=config.openai_key.get_secret_value(),
    api_version=config.azure_api_version,
    azure_endpoint=config.openai_base_url,
)
