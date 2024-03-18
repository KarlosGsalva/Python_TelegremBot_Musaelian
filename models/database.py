from datetime import date, time

from sqlalchemy import select, update, and_, delete
from sqlalchemy.ext.asyncio import create_async_engine

from models.models_core import users, events
from models.config import settings

from calendar_bot_db.support_funcs import hash_password
from typing import Optional

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
                                   echo=True, pool_size=5, max_overflow=10)


async def check_or_create_exists_user(user_tg_id: int) -> None:
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
                            event_details: str) -> None:
    try:
        async with async_engine.begin() as connection:
            await check_or_create_exists_user(user_tg_id)

            await connection.execute(events.insert().values(
                user_tg_id=user_tg_id, event_name=event_name,
                event_date=event_date, event_time=event_time,
                event_details=event_details))
    except Exception as e:
        print(f"Произошла ошибка в write_event_in_db {e}")
        return None


async def gather_all_events_db(user_tg_id: int) -> Optional[dict]:
    try:
        async with async_engine.begin() as connection:
            result = await connection.execute(
                select(events).where(events.c.user_tg_id == user_tg_id))

            # Переделываем словарь, чтобы обращаться к событиям по id
            events_data: dict = {event["id"]: event for event in result.mappings().all()}
            return events_data
    except Exception as e:
        print(f"Произошла ошибка в gather_all_events_db {e}")
        return None


async def read_selected_event(user_tg_id: int, event_id: int) -> Optional[str]:
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


async def change_event(user_tg_id: int, event_id: int,
                       new_event_name: Optional[str] = None,
                       new_event_date: Optional[date] = None,
                       new_event_time: Optional[time] = None,
                       new_event_details: Optional[str] = None) -> None:
    try:
        async with async_engine.begin() as connection:
            update_values: dict = {}
            if new_event_name is not None:
                update_values["event_name"] = new_event_name
            if new_event_date is not None:
                update_values["event_date"] = new_event_date
            if new_event_time is not None:
                update_values["event_time"] = new_event_time
            if new_event_details is not None:
                update_values["event_details"] = new_event_details

            await connection.execute(
                update(events).where(and_(events.c.id == event_id,
                                          events.c.user_tg_id == user_tg_id)).
                values(**update_values))
    except Exception as e:
        print(f"Произошла ошибка в delete_event {e}")
        return None


async def delete_event(user_tg_id: int, event_id: int) -> None:
    try:
        async with async_engine.begin() as connection:
            await connection.execute(
                delete(events).where(and_(events.c.user_tg_id == user_tg_id,
                                          events.c.id == event_id)))
    except Exception as e:
        print(f"Произошла ошибка в delete_event {e}")
        return None


async def save_registry_user_data(user_tg_id: int,
                                  username: Optional[str] = None,
                                  user_email: Optional[str] = None,
                                  user_password: Optional[str] = None) -> None:
    try:
        async with async_engine.begin() as connection:
            update_values = {}
            if username is not None:
                update_values["username"] = username
            if user_email is not None:
                update_values["email"] = user_email
            if user_password is not None:
                update_values["password_hash"] = hash_password(user_password)

            await connection.execute(
                update(users).where(users.c.user_tg_id == user_tg_id).
                values(**update_values))
    except Exception as e:
        print(f"Произошла ошибка в enter_user_data {e}")
        return None
