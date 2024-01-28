from os import path, listdir, remove
from sys import stdin

from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS


class NotesApp:
    def __init__(self) -> None:
        self.note_name = None
        self.note_text = None
        self.MENU_TEXT: dict = MENU_TEXT
        self.NOTIFICATIONS: dict = NOTIFICATION_TEXTS

    def read_notes(self) -> None:
        self.display_notes()
        requested_note = self.request_note_name_for_read()
        if path.isfile(f"{requested_note}"):
            with open(f"{requested_note}", "r", encoding="utf-8") as note_file:
                for line in note_file:
                    print(line.strip())
        else:
            print(self.NOTIFICATIONS["note_not_exist"])
            self.read_notes()

    def edit_note(self) -> None:
        requested_note = self.request_note_name_for_edit()
        if path.isfile(requested_note):
            self.show_note_content(requested_note)
            self.create_note(requested_note)
        else:
            print(self.NOTIFICATIONS["note_not_exist"])
            self.edit_note()

    def create_note(self, note_name=None) -> None:
        if note_name is None:
            note_name = input(self.NOTIFICATIONS["new_note_name"]) + "_note.txt"

        with open(f"{note_name}", "w", encoding="utf-8") as note_file:
            print(self.NOTIFICATIONS["request_note_text"])
            line = stdin.readline()

            while line != '\n':
                note_file.write(line)
                line = stdin.readline()

            print(self.NOTIFICATIONS["enter_finished"])
        print(f"Заметка {note_name} создана")

    def delete_note(self) -> None:
        requested_note = self.request_note_name_for_delete()
        if path.isfile(requested_note):
            remove(requested_note)
            print(f"\nЗаметка {requested_note} удалена")
        else:
            print(self.NOTIFICATIONS["note_not_exist"])
            self.delete_note()

    @staticmethod
    def show_note_content(note_name) -> None:
        with open(f"{note_name}", "r", encoding="utf-8") as note_file:
            for line in note_file:
                print(line.strip())

    @staticmethod
    def read_note_content(note_name) -> str:
        with open(f"{note_name}", "r", encoding="utf-8") as note_file:
            return note_file.read()

    @staticmethod
    def gather_all_notes() -> list:
        return [file for file in listdir(path.dirname(__file__)) if file.endswith('note.txt')]

    def display_notes(self) -> None:
        print(self.NOTIFICATIONS["accessed_notes"])
        for note in sorted(self.make_dict_for_sort().items(), key=lambda x: x[1]):
            print(note[0])

    def display_sorted_notes(self) -> None:
        print(self.NOTIFICATIONS["sorted_notes"])
        for note in sorted(self.make_dict_for_sort().items(), key=lambda x: x[1], reverse=True):
            print(note[0])

    def make_dict_for_sort(self) -> dict:
        return {k: len(self.read_note_content(k)) for k in self.gather_all_notes()}

    def request_note_name_for_read(self) -> str:
        note_name = input(self.NOTIFICATIONS["request_note_read"])
        return f"{note_name}_note.txt"

    def request_note_name_for_edit(self) -> str:
        note_name = input(self.NOTIFICATIONS["request_note_edit"])
        return f"{note_name}_note.txt"

    def request_note_name_for_delete(self) -> str:
        note_name = input(self.NOTIFICATIONS["request_note_delete"])
        return f"{note_name}_note.txt"

    def show_menu(self) -> None:
        for menu_point, menu_text in self.MENU_TEXT.items():
            print(f"{menu_point}: {menu_text}")

    def request_command(self) -> str:
        print(self.NOTIFICATIONS["choice_menu_point"])
        self.show_menu()

        user_choice = input(self.NOTIFICATIONS["enter_menu_point"])
        return user_choice


def main() -> None:
    notes_app = NotesApp()
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


try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    print("\n\nExiting... работа приложения прекращена командой консоли")
