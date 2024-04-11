from sqlalchemy import (Column, Integer, String, Table,
                        MetaData, Date, Time, ForeignKey, CheckConstraint)
from sqlalchemy.sql import func


metadata_obj = MetaData()

users = Table(
    "users", metadata_obj,
    Column("id", Integer(), primary_key=True),
    Column("user_tg_id", Integer(), unique=True),
    Column("username", String(40)),
    Column("email", String(40)),
    Column("password_hash", String(150)),
)

events = Table(
    "events", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_tg_id", Integer, ForeignKey("users.user_tg_id")),
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
)

