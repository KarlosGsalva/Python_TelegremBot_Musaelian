from datetime import time


def convert_str_to_time(chosen_time: str):
    new_event_time = time(*[int(tm) for tm in chosen_time.split(":")])
    return new_event_time


def split_callback_to_name_id(callback: str) -> dict:
    event_name, event_id = callback.split("_")
    return {"event_name": event_name, "event_id": int(event_id)}

