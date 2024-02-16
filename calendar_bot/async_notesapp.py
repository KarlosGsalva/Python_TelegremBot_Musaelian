import aiofiles
import aiofiles.os
import asyncio

from os import path, listdir, remove
from sys import stdin

from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS


class AsyncNotesApp:
    def __init__(self) -> None:
        self.note_name = None
        self.note_text = None
        self.MENU_TEXT: dict = MENU_TEXT
        self.NOTIFICATIONS: dict = NOTIFICATION_TEXTS

    async def create_note(self, note_name=None, note_text=None) -> None:
        try:
            if note_name is None:
                note_name = 'default_note_name' + '_note.txt'

            if note_text is None:
                note_text = 'example note content'

            async with aiofiles.open(f"{note_name}_note.txt", "a", encoding="utf-8") as note_file:
                await note_file.write(note_text)
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    async def delete_note(self, note) -> None:
        try:
            await aiofiles.os.remove(note)
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    def request_note_name_for_delete(self, note_name=None) -> str:
        try:
            if note_name is None:
                note_name = input(self.NOTIFICATIONS["request_note_delete"])
            return f"{note_name}_note.txt"
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

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

    # собираем список заметок из текущей директории
    # если директория не указана
    @staticmethod
    def gather_all_notes(main_path=None) -> list:
        try:
            if main_path is None:
                main_path = path.dirname(__file__)
            return [note for note in listdir(main_path) if note.endswith('note.txt')]
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
            notes = self.gather_all_notes()
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
