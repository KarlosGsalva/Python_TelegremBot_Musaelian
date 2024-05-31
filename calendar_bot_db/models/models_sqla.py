from sqlalchemy import (Column, Integer, String, Table, Interval,
                        MetaData, Date, Time, ForeignKey, CheckConstraint, BigInteger, UniqueConstraint)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ENUM


metadata_obj = MetaData()

users = Table(
    "users", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_tg_id", BigInteger, unique=True),
    Column("username", String(40)),
    Column("email", String(40)),
    Column("password_hash", String(150)),
)

events = Table(
    "events", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_tg_id", BigInteger, ForeignKey(
        "users.user_tg_id", ondelete="CASCADE")),
    Column("event_name", String, nullable=False, unique=True),
    Column("event_date", Date, default=func.current_date()),
    Column("event_time", Time, default=func.current_time()),
    Column("event_details", String),
)

botstatistics = Table(
    "botstatistics", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("date", Date, default=func.current_date()),
    Column("user_count", Integer, CheckConstraint("user_count >= 0")),
    Column("event_count", Integer, CheckConstraint("event_count >= 0")),
    Column("edited_events", Integer, CheckConstraint("edited_events >= 0")),
    Column("canceled_events", Integer, CheckConstraint("canceled_events >= 0")),
    Column("meeting_count", Integer, CheckConstraint("canceled_events >= 0")),
    Column("edited_meetings", Integer, CheckConstraint("canceled_events >= 0")),
    Column("canceled_meetings", Integer, CheckConstraint("canceled_events >= 0")),
)

participant_status_enum = ENUM('CF', 'CL', 'PD', name='meetingstatus', metadata=metadata_obj)

meetings = Table(
    "meetings", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_tg_id", BigInteger, ForeignKey(
        "users.user_tg_id", ondelete="CASCADE"), nullable=False),
    Column("event_id", Integer, ForeignKey("events.id"), nullable=True),
    Column("meeting_name", String, nullable=False),
    Column("date", Date, nullable=False),
    Column("time", Time, nullable=False),
    Column("duration", Interval, default="00:15:00", nullable=False),
    Column("end_time", Time, nullable=False),
    Column("details", String, nullable=True)
)

meeting_participants = Table(
    "meeting_participants", metadata_obj,
    Column("meeting_id", Integer, ForeignKey(
        "meetings.id", ondelete="CASCADE"), primary_key=True),
    Column("user_tg_id", BigInteger, ForeignKey(
        "users.user_tg_id", ondelete="CASCADE"), primary_key=True),
    Column("status", participant_status_enum, default="PD", nullable=False),
    UniqueConstraint('meeting_id', 'user_tg_id', name='uix_meeting_participants')
)
