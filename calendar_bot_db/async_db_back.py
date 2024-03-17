import aiofiles as aiof
import aiofiles.os as aiof_os

from datetime import time
import json
import pathlib


def convert_str_to_time(chosen_time: str):
    new_event_time = time(*[int(tm) for tm in chosen_time.split(":")])
    return new_event_time


# Функция записи события в json файл
# async def write_event_in_db(event_name: str,
#                             event_date: date = None,
#                             event_time: str = None,
#                             event_details: str = None) -> None:
#     try:
#         formatted_date = event_date if event_date else "Дата не указана"
#         formatted_time = event_time if event_time else "Время не указано"
#         formatted_details = event_details if event_details else "Описание отсутствует"
#
#         dump_object = {event_name: {"Дата события": formatted_date,
#                                     "Время события": formatted_time,
#                                     "Описание события": formatted_details}}
#
#         async with aiof.open(f"{event_name}.json", mode="w", encoding="utf-8") as json_file:
#             await json_file.write(json.dumps(dump_object, ensure_ascii=False, indent=4))
#     except Exception as e:
#         print(f"Произошла ошибка{e}")


# Чтение имеющихся событий в указанной или базовой директории
# def gather_having_events(path_for_search=None) -> list[str]:
#     try:
#         if path_for_search is None:
#             path_for_search = pathlib.Path(__file__).parent
#         else:
#             path_for_search = pathlib.Path(path_for_search)
#
#         events: list = [event.name for event in path_for_search.glob("*.json")]
#         return events
#     except Exception as e:
#         print(f"Произошла ошибка{e}")


# Читаем запрошенное событие из файла
# async def read_event(event_name: str) -> dict:
#     try:
#         async with aiof.open(f"{event_name}", mode="r", encoding="utf-8") as json_file:
#             content = await json_file.read()
#             event_data = json.loads(content)
#         return event_data
#     except Exception as e:
#         print(f"Произошла ошибка{e}")


# Форматируем словарь для вывода пользователю
# def format_event_data(event_data: dict) -> str:
#     try:
#         event_name = ''.join(event_data.keys())
#         event_details = "\n".join(f"{name}: {text}" for name, text in event_data[event_name].items())
#         return event_name + "\n" + event_details
#     except Exception as e:
#         print(f"Произошла ошибка{e}")


# Изменяем выбранный пункт события
async def change_event_point(event_name: str, event_point: str, new_data: str) -> None:
    try:
        async with aiof.open(f"{event_name}.json", mode="r", encoding="utf-8") as old_event:
            old_data = await old_event.read()
            deserialised_data = json.loads(old_data)

        deserialised_data[event_name][event_point] = new_data

        async with aiof.open(f"{event_name}.json", mode="w", encoding="utf-8") as new_event:
            await new_event.write(json.dumps(deserialised_data))
    except Exception as e:
        print(f"Произошла ошибка{e}")


# Удаляем событие
async def delete_event(event_name: str) -> None:
    try:
        await aiof_os.remove(event_name)
    except Exception as e:
        print(f"Произошла ошибка{e}")








