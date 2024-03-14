from datetime import date, time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from models.models_core import metadata_obj, users, events
from config import settings

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
    try:
        async with async_engine.begin() as connection:
            await check_and_create_exists_user(user_tg_id)

            await connection.execute(events.insert().values(
                user_tg_id=user_tg_id, event_name=event_name,
                event_date=event_date, event_time=event_time,
                event_details=event_details))
    except Exception as e:
        print(f"Произошла ошибка в write_event_in_db {e}")


async def gather_all_events_db(user_tg_id: int) -> dict:
    try:
        async with async_engine.begin() as connection:
            result = await connection.execute(
                select(events).where(events.c.user_tg_id == user_tg_id))
            events_data: dict = {event["id"]: event for event in result.mappings().all()}
            # print(events_data)
            return events_data
    except Exception as e:
        print(f"Произошла ошибка в gather_all_events_db {e}")


async def read_choosed_event(user_tg_id: int, event_id: int) -> str:
    try:
        events: dict = await gather_all_events_db(user_tg_id)

        event_name = f'Событие: {events[event_id]["event_name"]}'
        event_date = f'Дата события: {date.strftime(events[event_id]["event_date"], "%d.%m.%Y")}'
        event_time = f'Время события: {time.strftime(events[event_id]["event_time"], "%H:%M")}'
        event_details = f'Описание: {events[event_id]["event_details"]}'

        return '\n'.join([event_name, event_date, event_time, event_details])
    except Exception as e:
        print(f"Произошла ошибка в read_choosed_event {e}")

# asyncio.run(async_main())
# asyncio.run(gather_all_events_db(1074713049))
