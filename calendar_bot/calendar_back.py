import datetime
import os


class Calendar:
    def __init__(self):
        self.events = {}

    def create_event(self, event_name: str,
                     event_date: datetime.date,
                     event_time: datetime.time,
                     event_details: str) -> int:
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "name": event_name,
            "date": event_date,
            "time": event_time,
            "details": event_details
        }
        self.events[event_id] = event
        return event_id

    def read_event(self, event_id: int) -> dict | str:
        event = self.events.get(event_id)
        if event:
            return event
        return "Такого события нет или произошла ошибка"

    def edit_event(self, event_id: int,
                   event_name: str = None,
                   event_date: datetime.date = None,
                   event_time: datetime.time = None,
                   event_details: str = None) -> str:
        if event_id in self.events:
            if event_name:
                self.events[event_id]["name"] = event_name
            if event_date:
                self.events[event_id]["date"] = event_date
            if event_time:
                self.events[event_id]["time"] = event_time
            if event_details:
                self.events[event_id]["details"] = event_details
            return "Событие успешно обновлено"
        return "Такого события нет или произошла ошибка"

    def delete_event(self, event_id: int) -> str:
        if event_id in self.events:
            del self.events[event_id]
            return "Событие успешно удалено"
        return "Такого события нет или произошла ошибка"

    def show_events(self, event_id: int) -> str | None:
        if event_id in self.events:
            for event_id, event in self.events.items():
                print(event_id, end=' ')
                for key, details in event.items():
                    print(f'{key}: {details}')
            return
        return "Список событий пуст или произошла ошибка"
