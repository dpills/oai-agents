from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from openai import AsyncOpenAI

from .config import config

db: AsyncIOMotorDatabase[Any] = AsyncIOMotorClient(config.mongo_uri.get_secret_value())[
    config.mongo_db
]

openai_client = AsyncOpenAI(api_key=config.openai_key.get_secret_value())
