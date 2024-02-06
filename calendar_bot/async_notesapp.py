import asyncio
import aiofiles
from os import path, listdir, remove
from sys import stdin

from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS


class AsyncNotesApp:
    def __init__(self) -> None:
        self.note_name = None
        self.note_text = None
        self.MENU_TEXT: dict = MENU_TEXT
        self.NOTIFICATIONS: dict = NOTIFICATION_TEXTS

    def read_notes(self) -> None:
        try:
            self.display_notes()
            requested_note = self.request_note_name_for_read()
            if path.isfile(requested_note):
                with open(requested_note, "r", encoding="utf-8") as note_file:
                    for line in note_file:
                        print(line.strip())
            else:
                print(self.NOTIFICATIONS["note_not_exist"])
                self.read_notes()
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def edit_note(self) -> None:
        try:
            requested_note = self.request_note_name_for_edit()
            if path.isfile(requested_note):
                self.show_note_content(requested_note)
                self.create_note(requested_note)
            else:
                print(self.NOTIFICATIONS["note_not_exist"])
                self.edit_note()
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def create_note(self, note_name=None) -> None:
        try:
            if note_name is None:
                note_name = input(self.NOTIFICATIONS["new_note_name"]) + "_note.txt"

            with open(note_name, "w", encoding="utf-8") as note_file:
                print(self.NOTIFICATIONS["request_note_text"])
                line = stdin.readline()

                while line != '\n':
                    note_file.write(line)
                    line = stdin.readline()

                print(self.NOTIFICATIONS["enter_finished"])
            print(f"Заметка {note_name} создана")
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def delete_note(self) -> None:
        try:
            requested_note = self.request_note_name_for_delete()
            if path.isfile(requested_note):
                remove(requested_note)
                print(f"\nЗаметка {requested_note} удалена")
            else:
                print(self.NOTIFICATIONS["note_not_exist"])
                self.delete_note()
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    @staticmethod
    def show_note_content(note_name) -> None:
        try:
            with open(note_name, "r", encoding="utf-8") as note_file:
                for line in note_file:
                    print(line.strip())
        except Exception as e:
            print('Произошла ошибка', e)

    @staticmethod
    async def read_note_content(note_name) -> str:
        try:
            # Используем aiofiles для асинхронного открытия и чтения файла
            async with aiofiles.open(note_name, mode="r", encoding="utf-8") as note_file:
                content = await note_file.read()
            return content
        except Exception as e:
            print('Произошла ошибка', e)
            return ""

    @staticmethod
    async def gather_all_notes() -> list:
        try:
            # Используем asyncio.to_thread для асинхронного выполнения синхронной функции
            files = await asyncio.to_thread(
                lambda: [file for file in listdir(path.dirname(__file__)) if file.endswith('note.txt')]
            )
            return files
        except Exception as e:
            print('Произошла ошибка', e)
            return []

    def display_notes(self) -> None:
        try:
            print(self.NOTIFICATIONS["accessed_notes"])
            for note in sorted(self.make_dict_for_sort().items(), key=lambda x: x[1]):
                print(note[0])
        except Exception as e:
            print('Произошла ошибка', e)

    async def display_sorted_notes(self, bot, chat_id):
        try:
            print(self.NOTIFICATIONS["sorted_notes"])
            dict_for_sort = await self.make_dict_for_sort()
            # Выполняем сортировку синхронно
            for note in sorted(dict_for_sort.items(), key=lambda x: x[1], reverse=True):
                # Используем асинхронную отправку сообщений через бот
                await bot.send_message(chat_id, note[0])
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    async def make_dict_for_sort(self) -> dict:
        try:
            # Сначала получаем список заметок асинхронно
            notes = await self.gather_all_notes()
            # Теперь нам нужно асинхронно прочитать содержимое каждой заметки.
            # Используем асинхронное списковое включение с asyncio.gather для выполнения всех
            # асинхронных операций чтения содержимого заметок
            contents = await asyncio.gather(*(self.read_note_content(note) for note in notes))
            # Возвращаем словарь, где ключи - имена заметок, а значения - длина их содержимого
            return {note: len(content) for note, content in zip(notes, contents)}
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)
            return {}

    def request_note_name_for_read(self) -> str:
        try:
            note_name = input(self.NOTIFICATIONS["request_note_read"])
            return f"{note_name}_note.txt"
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def request_note_name_for_edit(self) -> str:
        try:
            note_name = input(self.NOTIFICATIONS["request_note_edit"])
            return f"{note_name}_note.txt"
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def request_note_name_for_delete(self) -> str:
        try:
            note_name = input(self.NOTIFICATIONS["request_note_delete"])
            return f"{note_name}_note.txt"
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def show_menu(self) -> None:
        try:
            for menu_point, menu_text in self.MENU_TEXT.items():
                print(f"{menu_point}: {menu_text}")
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def request_command(self) -> str:
        try:
            print(self.NOTIFICATIONS["choice_menu_point"])
            self.show_menu()

            user_choice = input(self.NOTIFICATIONS["enter_menu_point"])
            return user_choice
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)


def main() -> None:
    try:
        notes_app = AsyncNotesApp()
        while True:
            entered_command = notes_app.request_command()
            match entered_command:
                case '1':
                    notes_app.create_note()
                case '2':
                    notes_app.read_notes()
                case '3':
                    notes_app.edit_note()
                case '4':
                    notes_app.delete_note()
                case '5':
                    notes_app.display_sorted_notes()
                case '6':
                    print(notes_app.NOTIFICATIONS["bye"])
                    break
                case _:
                    print(notes_app.NOTIFICATIONS["incorrect_menu_point"])
    except Exception as e:
        print('Произошла ошибка', e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... работа приложения прекращена командой консоли")