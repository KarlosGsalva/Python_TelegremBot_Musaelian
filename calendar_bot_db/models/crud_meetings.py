import logging

from datetime import time, timedelta
from datetime import datetime as dt

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
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

        logger.debug(f"result в is_user_available {end_time, type(end_time)}")

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

        logger.debug(f"result в is_user_available {result}")

        return result.rowcount == 0
    except Exception as e:
        logger.debug(f"Ошибка в is_user_available {e}")
        return None


async def get_user_busy_slots(user_tg_id):
    try:
        async with async_engine.begin() as connection:
            query = select(
                meetings.c.meeting_name,
                meetings.c.date,
                meetings.c.time,
                meetings.c.duration,
                meetings.c.end_time,
                meetings.c.details
            ).select_from(meetings.join(meeting_participants)).where(
                and_(
                    meeting_participants.c.user_tg_id == user_tg_id,
                    meeting_participants.c.status == "CF"
                )
            )

            result = await connection.execute(query)
            rows = result.fetchall()

            busy_slots = [(row.meeting_name,
                           row.date,
                           row.time,
                           row.duration,
                           row.end_time,
                           row.details)
                          for row in rows]

            # Форматирование вывода
            formatted_slots = "\n".join(
                f"Meeting: {slot[0]}\n"
                f"Date: {slot[1]}\n"
                f"Time: {slot[2]}\n"
                f"Duration: {slot[3]}\n"
                f"End time: {slot[4]}\n"
                f"Details: {slot[5]}\n"
                for slot in busy_slots
            )

            return formatted_slots
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
                    "username": row.username if row.username else str(row.user_tg_id)}

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
        meeting_date = dt.strptime(meeting_date, "%d.%m.%Y").date()
        duration_interval = timedelta(minutes=int(meeting_duration))

        start_datetime = dt.combine(meeting_date, meeting_time)
        end_datetime = start_datetime + duration_interval
        end_time = end_datetime.time()

        async with async_engine.begin() as connection:
            # Запись митинга в таблицу meetings
            result = await connection.execute(
                insert(meetings).values(
                    user_tg_id=organizer,
                    meeting_name=meeting_name,
                    date=meeting_date,
                    time=meeting_time,
                    duration=duration_interval,
                    end_time=end_time,
                    details=meeting_details,
                ).returning(meetings.c.id)
            )
            meeting_id = result.scalar()

            # Запись участников митинга
            for participant_id in participants:
                await connection.execute(
                    insert(meeting_participants).values(
                        meeting_id=meeting_id,
                        user_tg_id=participant_id,
                        status='PD'
                    )
                )
            return meeting_id
    except Exception as e:
        logger.debug(f"Произошла ошибка в write_meeting_in_db {e}")
        return None


async def accept_decline_invite(participant_id: int, meeting_id: int,
                                accept=False, decline=False):
    try:
        async with async_engine.begin() as connection:
            if accept:
                confirmed = "CF"
                query = (update(meeting_participants)
                         .where(meeting_participants.c.meeting_id == meeting_id,
                                meeting_participants.c.user_tg_id == participant_id)
                         .values(status=confirmed))

            elif decline:
                canceled = "CL"
                query = (update(meeting_participants)
                         .where(meeting_participants.c.meeting_id == meeting_id,
                                meeting_participants.c.user_tg_id == participant_id)
                         .values(status=canceled))

            else:
                logger.debug("Не указаны accept или decline, статус не изменен.")
                return None

            await connection.execute(query)
    except Exception as e:
        logger.debug(f"Произошла ошибка в accept_decline_invite {e}")
        return None
