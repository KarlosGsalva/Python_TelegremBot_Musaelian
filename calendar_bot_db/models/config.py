import logging

from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker
# from sqlalchemy.ext.asyncio import AsyncSession


class Settings(BaseSettings):
    bot_token: SecretStr
    DB_URL: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

logger = logging.getLogger(__name__)

redis = Redis.from_url("redis://redis:6379/4")
storage = RedisStorage(redis, DefaultKeyBuilder(with_destiny=True))

async_engine = create_async_engine(url=settings.DB_URL, echo=True)

# для работы с sqla_orm
# session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
