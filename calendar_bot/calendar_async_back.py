import aiogram as aio
import aiofiles as aiof

from datetime import date
import json


# Функция записи события в текстовый файл
async def write_event_in_txt_file(event_name: str,
                                  event_date: date = None,
                                  event_time: str = None,
                                  event_details: str = None):
    formatted_date = event_date if event_date else "Дата не указана"
    formatted_time = event_time if event_time else "Время не указано"
    formatted_details = event_details if event_details else "Описание отсутствует"
    full_data = (f"Событие {event_name}\n"
                 f"Дата события {formatted_date}\n"
                 f"Время события {formatted_time}\n"
                 f"Описание события {formatted_details}")

    async with aiof.open(f"{event_name}.txt", mode="w", encoding="utf-8") as event_file:
        await event_file.write(full_data)


# Функция записи события в json файл
async def write_event_in_json_file(event_name: str,
                                   event_date: date = None,
                                   event_time: str = None,
                                   event_details: str = None):
    formatted_date = event_date if event_date else "Дата не указана"
    formatted_time = event_time if event_time else "Время не указано"
    formatted_details = event_details if event_details else "Описание отсутствует"

    dump_object = {event_name: {"Дата события": formatted_date,
                                "Время события": formatted_time,
                                "Описание события": formatted_details}}

    async with aiof.open(f"{event_name}.json", mode="w", encoding="utf-8") as json_file:
        await json_file.write(json.dumps(dump_object, ensure_ascii=False, indent=4))


