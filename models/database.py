import asyncio
from datetime import date, time
from typing import Optional

from sqlalchemy import Insert, select
from sqlalchemy.ext.asyncio import create_async_engine

from models.models_core import metadata_obj, users, events
from models.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
                                   echo=True, pool_size=5, max_overflow=10)


async def async_main() -> None:
    async with async_engine.begin() as connection:
        await connection.run_sync(metadata_obj.create_all)

        await connection.execute(
            users.insert(), {
                "user_tg_id": 1, "username": "test",
                "password_hash": "qwerty"})

        await async_engine.dispose()


async def check_and_create_exists_user(user_tg_id: int) -> None:
    async with async_engine.begin() as connection:
        stmt = select(users).where(users.c.user_tg_id == user_tg_id)
        result = await connection.execute(stmt)
        user = result.fetchone()

        if user is None:
            stmt = users.insert().values(user_tg_id=user_tg_id)
            await connection.execute(stmt)
            print("user was created")
        else:
            print("user already exists")


async def write_event_in_db(user_tg_id: int,
                            event_name: str,
                            event_date: date,
                            event_time: time,
                            event_details: str):
    async with async_engine.begin() as connection:
        await check_and_create_exists_user(user_tg_id)

        await connection.execute(events.insert().values(
            user_tg_id=user_tg_id, event_name=event_name,
            event_date=event_date, event_time=event_time,
            event_details=event_details))
        await async_engine.dispose()

# asyncio.run(async_main())
