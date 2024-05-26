import logging

from datetime import time, timedelta
from datetime import datetime as dt

from sqlalchemy import select, update, and_, delete, or_, not_, insert
from sqlalchemy.sql import func

from calendar_bot_db.models.models_core import users, events, botstatistics, meetings, meeting_participants
from calendar_bot_db.models.config import async_engine

from calendar_bot_db.services import hash_password
from typing import Optional

logger = logging.getLogger(__name__)


async def is_user_available(connection, user_tg_id, date, start_time, duration):
    try:
        end_time = (dt.combine(date, start_time) + duration).time()
        # ---------------
        logger.debug(f"result в is_user_available {end_time, type(end_time)}")
        # ---------------
        query = select([meetings]).select_from(meetings.join(meeting_participants)).where(
            and_(
                meeting_participants.c.participant_id == user_tg_id,
                meetings.c.status == "CF",
                meetings.c.date == date,
                not_(or_(
                    end_time <= meetings.c.time,
                    start_time >= (meetings.c.time + meetings.c.duration)
                ))))

        result = connection.execute(query)
        # ---------------
        logger.debug(f"result в is_user_available {result}")
        # ---------------
        return result.rowcount == 0
    except Exception as e:
        logger.debug(f"Ошибка в is_user_available {e}")
        return None


async def get_user_busy_slots(user_tg_id):
    try:
        async with async_engine.begin() as connection:
            query = (select([meetings.c.date, meetings.c.time, meetings.c.duration])
            .where(and_(
                meetings.c.user_tg_id == user_tg_id,
                meetings.c.status == "CF")))

            result = connection.execute(query)
            # ---------------
            logger.debug(f"result в get_user_busy_slots {result, type(result)}")
            # ---------------
        busy_slots = [(row.date, row.time, row.duration) for row in result]
        return busy_slots
    except Exception as e:
        logger.debug(f"Ошибка в get_user_busy_slots {e}")
        return None


async def book_meeting(organizer, participant_ids, date,
                       start_time, duration, details, event_id=None):
    try:
        checked_participants = []
        async with async_engine.begin() as connection:
            for participant_id in participant_ids:
                if not is_user_available(connection, participant_id, date, start_time, duration):
                    checked_participants.append(participant_id)

            create_meeting = insert(meetings).values(
                organizer=organizer,
                date=date,
                time=start_time,
                duration=duration,
                details=details,
                event_id=event_id
            )
            result = connection.execute(create_meeting)
            meeting_id = result.inserted_primary_key[0]

            participants_data = [
                {"meeting_id": meeting_id, "participant_id": participant_id}
                for participant_id in participant_ids
            ]

            connection.execute(insert(meeting_participants), participants_data)
    except Exception as e:
        logger.debug(f"Ошибка в book_meeting {e}")
        return None


async def gather_all_users_db(user_tg_id: int) -> Optional[dict]:
    try:
        async with async_engine.begin() as connection:
            query = select(
                users.c.user_tg_id,
                users.c.username
            ).where(users.c.user_tg_id != user_tg_id)

            result = await connection.execute(query)
            logger.debug(f"result = {result}, result_type = {type(result)}")

            user_data = {}
            for row in result:
                user_data[row.user_tg_id] = {
                    "user_id": str(row.user_tg_id),
                    "username": str(row.username) if row.username else str(row.user_tg_id)}

            return user_data
    except Exception as e:
        logger.debug(f"Произошла ошибка в gather_all_users_db {e}")
        return None


async def write_meeting_in_db(organizer: int,
                              meeting_name: str,
                              meeting_date: str,
                              meeting_time: time,
                              meeting_duration: str,
                              meeting_details: str,
                              participants: list) -> None:
    try:
        event_date = dt.strptime(meeting_date, "%d.%m.%Y").date()
        duration_interval = timedelta(minutes=int(meeting_duration))

        async with async_engine.begin() as connection:
            # Запись митинга в таблицу meetings
            result = await connection.execute(
                insert(meetings).values(
                    user_tg_id=organizer,
                    meeting_name=meeting_name,
                    date=event_date,
                    time=meeting_time,
                    duration=duration_interval,
                    details=meeting_details,
                    status='PD'
                ).returning(meetings.c.id)
            )
            meeting_id = result.scalar()

            # Запись участников митинга
            for participant_id in participants:
                await connection.execute(
                    insert(meeting_participants).values(
                        meeting_id=meeting_id,
                        user_tg_id=participant_id
                    )
                )

    except Exception as e:
        logger.debug(f"Произошла ошибка в write_meeting_in_db {e}")
        return None