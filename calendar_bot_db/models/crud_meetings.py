import logging

from datetime import time, timedelta
from datetime import datetime as dt

from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from sqlalchemy import select, update, and_, delete, or_, not_, insert
from sqlalchemy.sql import func

from calendar_bot_db.models.models_sqla import users, events, botstatistics, meetings, meeting_participants
from calendar_bot_db.models.config import async_engine

from calendar_bot_db.services import hash_password
from typing import Optional

logger = logging.getLogger(__name__)


async def is_user_available(connection, user_tg_id, date, start_time, duration):
    try:
        user_tg_id = int(user_tg_id)
        end_time = (dt.combine(date, start_time) + duration).time()

        query = select(meetings.c.id).select_from(meetings.join(meeting_participants)).where(
            and_(
                meeting_participants.c.user_tg_id == user_tg_id,
                meeting_participants.c.status == "CF",
                meetings.c.date == date,
                and_(
                    meetings.c.time <= end_time,
                    meetings.c.end_time >= start_time)
            )
        )

        result = await connection.execute(query)
        slots = result.fetchall()

        return len(slots) != 0
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

            busy_slots = ((row.meeting_name,
                           row.date,
                           row.time,
                           row.duration,
                           row.end_time,
                           row.details)
                          for row in rows)

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


async def gather_user_meetings_db(user_tg_id: int) -> Optional[dict]:
    try:
        async with async_engine.begin() as connection:
            result = await connection.execute(
                select(meetings).where(meetings.c.user_tg_id == user_tg_id))

            # Переделываем словарь, чтобы обращаться к встречам по id
            meetings_data: dict = {event["id"]: event for event in result.mappings().all()}
            logger.debug(f"meetings_data в gather_user_meetings_db = {meetings_data}")
            return meetings_data
    except Exception as e:
        logger.debug(f"Произошла ошибка в gather_user_meetings_db {e}")
        return None


async def delete_meeting(user_tg_id: int, meeting_id: int) -> None:
    try:
        async with async_engine.begin() as connection:
            await connection.execute(
                delete(meetings).where(
                    and_(meetings.c.user_tg_id == user_tg_id,
                         meetings.c.id == meeting_id))
            )
    except Exception as e:
        logger.debug(f"Произошла ошибка в delete_meeting {e}")
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


# --------------------------------

async def change_events_visibility(user_tg_id: int,
                                   events_to_publish: list,
                                   publish=False) -> Optional[dict]:
    try:
        async with async_engine.begin() as connection:
            visibility = "PB" if publish else "PR"
            current_visibility = "PR" if publish else "PB"

            for event in events_to_publish:
                if event.startswith("Событие"):
                    event_name = " ".join(event.split()[1:])
                    query = update(events).where(
                        events.c.user_tg_id == user_tg_id,
                        events.c.event_name == event_name,
                        events.c.visibility == current_visibility
                    ).values(visibility=visibility)

                elif event.startswith("Встреча"):
                    meeting_name = " ".join(event.split()[1:])
                    query = update(meetings).where(
                        meetings.c.user_tg_id == user_tg_id,
                        meetings.c.meeting_name == meeting_name,
                        meetings.c.visibility == current_visibility
                    ).values(visibility=visibility)

                else:
                    continue

                result = await connection.execute(query)
                logger.debug(f"Query: {query}")
                logger.debug(f"Rows affected: {result.rowcount}")

    except Exception as e:
        logger.debug(f"Произошла ошибка в change_event_visibility = {e}")
        return None

# --------------------------------


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

            # Записываем организатора со статусом подтверждено
            await connection.execute(
                insert(meeting_participants).values(
                    meeting_id=meeting_id,
                    user_tg_id=organizer,
                    status="CF"
                ))

            # Записываем приглашенных участников митинга
            for participant_id in participants:
                await connection.execute(
                    insert(meeting_participants).values(
                        meeting_id=meeting_id,
                        user_tg_id=participant_id,
                        status="PD"
                    ))

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


async def get_calendar_events(user_tg_id, for_keyboard=False, for_callback=False, private=True):
    try:
        async with async_engine.begin() as connection:
            if private:
                query_event = select(
                    events.c.event_name,
                    events.c.event_date,
                    events.c.event_time,
                    events.c.event_details
                ).where(
                    events.c.user_tg_id == user_tg_id,
                    events.c.visibility == "PR"
                )

                query_meeting = select(
                    meetings.c.meeting_name,
                    meetings.c.date,
                    meetings.c.time,
                    meetings.c.duration,
                    meetings.c.end_time,
                    meetings.c.details
                ).where(
                    meetings.c.user_tg_id == user_tg_id,
                    meetings.c.visibility == "PR"
                )
            else:
                query_event = select(
                    events.c.event_name,
                    events.c.event_date,
                    events.c.event_time,
                    events.c.event_details
                ).where(
                    events.c.user_tg_id == user_tg_id
                )

                query_meeting = select(
                    meetings.c.meeting_name,
                    meetings.c.date,
                    meetings.c.time,
                    meetings.c.duration,
                    meetings.c.end_time,
                    meetings.c.details
                ).where(
                    meetings.c.user_tg_id == user_tg_id
                )

            result_events = await connection.execute(query_event)
            events_data = result_events.fetchall()

            result_meetings = await connection.execute(query_meeting)
            meetings_data = result_meetings.fetchall()

            combined_data = []
            for row in events_data:
                combined_data.append({
                    "type": "Событие",
                    "name": row.event_name,
                    "date": row.event_date.strftime("%d.%m.%Y"),
                    "time": row.event_time.strftime("%H:%M"),
                    "details": row.event_details
                })

            for row in meetings_data:
                combined_data.append({
                    "type": "Встреча",
                    "name": row.meeting_name,
                    "date": row.date.strftime("%d.%m.%Y"),
                    "time": row.time.strftime("%H:%M"),
                    "duration": str(row.duration),
                    "end_time": row.end_time.strftime("%H:%M"),
                    "details": row.details
                })

            combined_data.sort(key=lambda x: (x["date"], x["time"], x["name"]))
            logger.debug(f"combined_data in get_calendar_events = {combined_data}")

            if for_keyboard:
                return combined_data

            if for_callback:
                events_data: dict = {}
                for event in combined_data:
                    events_data[event["name"]] = event
                return events_data

            result_string = ""
            for item in combined_data:
                if item["type"] == "Событие":
                    result_string += (f"Событие: {item['name']}\n"
                                      f"Дата: {item['date']}\n"
                                      f"Время: {item['time']}\n"
                                      f"Описание: {item['details']}\n\n")
                else:
                    result_string += (f"Встреча: {item['name']}\n"
                                      f"Дата: {item['date']}\n"
                                      f"Время: {item['time']}\n"
                                      f"Длительность: {item['duration']}\n"
                                      f"Время окончания: {item['end_time']}\n"
                                      f"Описание: {item['details']}\n")
            return result_string
    except Exception as e:
        logger.debug(f"Произошла ошибка в get_calendar_events {e}")
        return None
