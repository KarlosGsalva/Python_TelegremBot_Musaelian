from sqlalchemy import (Column, Integer, String, Table,
                        MetaData, Date, Time, ForeignKey)
from sqlalchemy.sql import func


metadata_obj = MetaData()

users = Table(
    "users", metadata_obj,
    Column("id", Integer(), primary_key=True),
    Column("user_tg_id", Integer(), unique=True),
    Column("username", String(40)),
    Column("email", String(40)),
    Column("password_hash", String(50)),
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

"""
result.mappings().all() -> 

[{'id': 1, 'user_tg_id': 1074713049, 
'event_name': 'test event', 
'event_date': datetime.date(2024, 3, 14), 
'event_time': datetime.time(20, 30), 
'event_details': 'asdf'}, 

{'id': 2, 'user_tg_id': 1074713049, 
'event_name': 'test event 2', 
'event_date': datetime.date(2024, 3, 15), 
'event_time': datetime.time(18, 30), 
'event_details': 'test text text test text test'}]

events_data: dict = 
{event["id"]: event for event in result.mappings().all()} -> 

{
    1: {'id': 1, 'user_tg_id': 1074713049, 
        'event_name': 'test event', 
        'event_date': datetime.date(2024, 3, 14), 
        'event_time': datetime.time(20, 30), 
        'event_details': 'asdf'}, 
        
    2: {'id': 2, 'user_tg_id': 1074713049, 
        'event_name': 'test event 2', 
        'event_date': datetime.date(2024, 3, 15), 
        'event_time': datetime.time(18, 30), 
        'event_details': 'test text text test text test'}
}

"""




