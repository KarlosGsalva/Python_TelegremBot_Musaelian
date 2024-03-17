from datetime import date, time

from sqlalchemy import select, update, and_
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
    try:
        async with async_engine.begin() as connection:
            await check_and_create_exists_user(user_tg_id)

            await connection.execute(events.insert().values(
                user_tg_id=user_tg_id, event_name=event_name,
                event_date=event_date, event_time=event_time,
                event_details=event_details))
    except Exception as e:
        print(f"Произошла ошибка в write_event_in_db {e}")
        return None


async def gather_all_events_db(user_tg_id: int) -> dict | None:
    try:
        async with async_engine.begin() as connection:
            result = await connection.execute(
                select(events).where(events.c.user_tg_id == user_tg_id))
            events_data: dict = {event["id"]: event for event in result.mappings().all()}
            # print(events_data)
            return events_data
    except Exception as e:
        print(f"Произошла ошибка в gather_all_events_db {e}")
        return None


async def read_choosed_event(user_tg_id: int, event_id: int) -> str | None:
    try:
        events: dict = await gather_all_events_db(user_tg_id)

        event_name = f'Событие: {events[event_id]["event_name"]}'
        event_date = f'Дата события: {date.strftime(events[event_id]["event_date"], "%d.%m.%Y")}'
        event_time = f'Время события: {time.strftime(events[event_id]["event_time"], "%H:%M")}'
        event_details = f'Описание: {events[event_id]["event_details"]}'

        return '\n'.join([event_name, event_date, event_time, event_details])
    except Exception as e:
        print(f"Произошла ошибка в read_choosed_event {e}")
        return None


async def rename_event(user_tg_id: int, event_id: int, new_event_name: str) -> None:
    try:
        async with async_engine.begin() as connection:
            await connection.execute(
                update(events).where(and_(events.c.id == event_id,
                                          events.c.user_tg_id == user_tg_id)).
                values(event_name=new_event_name))
    except Exception as e:
        print(f"Произошла ошибка в rename_event {e}")
        return None


async def change_event_date(user_tg_id: int, event_id: int, new_event_date: date) -> None:
    try:
        async with async_engine.begin() as connection:
            await connection.execute(
                update(events).where(and_(events.c.user_tg_id == user_tg_id,
                                          events.c.id == event_id)).
                values(event_date=new_event_date))
    except Exception as e:
        print(f"Произошла ошибка в change_event_date {e}")
        return None


async def change_event_time(user_tg_id: int, event_id: int, new_event_time: time):
    try:
        async with async_engine.begin() as connection:
            await connection.execute(
                update(events).where(and_(events.c.user_tg_id == user_tg_id,
                                          events.c.id == event_id)).
                values(event_time=new_event_time))
    except Exception as e:
        print(f"Произошла ошибка в change_event_time {e}")
        return None


async def change_event_details(user_tg_id: int, event_id: int, event_details: str) -> None:
    try:
        async with async_engine.begin() as connection:
            await connection.execute(
                update(events).where(and_(events.c.user_tg_id == user_tg_id,
                                          events.c.id == event_id)).
                values(event_details=event_details))
    except Exception as e:
        print(f"Произошла ошибка в change_event_time {e}")
        return None


# asyncio.run(async_main())
# asyncio.run(gather_all_events_db(1074713049))
