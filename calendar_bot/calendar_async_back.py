import aiofiles as aiof

from datetime import date
import json
import pathlib


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


# Чтение имеющихся событий в указанной или базовой директории
def gather_having_events(path_for_search=None):
    if path_for_search is None:
        path_for_search = pathlib.Path(__file__).parent
    else:
        path_for_search = pathlib.Path(path_for_search)

    events: list = [event.name for event in path_for_search.glob("*.json")]
    return events


# Читаем запрошенное событие из файла
async def read_event(event_name: str) -> dict:
    async with aiof.open(f"{event_name}", mode="r", encoding="utf-8") as json_file:
        content = await json_file.read()
        event_data = json.loads(content)
    return event_data


# Форматируем словарь для вывода пользователю
def format_event_data(event_data: dict) -> str:
    event_name = ''.join(event_data.keys())
    event_details = "\n".join(f"{name}: {text}" for name, text in event_data[event_name].items())
    return event_name + "\n" + event_details


# Изменяем выбранный пункт события
async def change_event_point(event_name: str, event_point: str, new_data: str) -> None:
    async with aiof.open(f"{event_name}.json", mode="r", encoding="utf-8") as old_event:
        old_data = await old_event.read()
        deserialised_data = json.loads(old_data)

    deserialised_data[event_name][event_point] = new_data

    async with aiof.open(f"{event_name}.json", mode="w", encoding="utf-8") as new_event:
        await new_event.write(json.dumps(deserialised_data))












