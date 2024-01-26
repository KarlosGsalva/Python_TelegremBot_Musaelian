from collections import defaultdict
from os import path, listdir, remove
from sys import stdin


class NotesApp:
    def __init__(self) -> None:
        self.note_name = None
        self.note_text = None

    def read_notes(self) -> None:
        self.show_existing_notes()
        requested_note = self.request_note_name_for_read()
        if path.isfile(f"{requested_note}"):
            with open(f"{requested_note}", "r", encoding="utf-8") as note_file:
                for line in note_file:
                    print(line.strip())
        else:
            self.not_exist_file_warning()
            self.read_notes()

    def edit_note(self) -> None:
        requested_note = self.request_note_name_for_edit()
        if path.isfile(requested_note):
            self.show_note_content(requested_note)
            self.create_note(requested_note)
        else:
            self.not_exist_file_warning()
            self.edit_note()

    @staticmethod
    def create_note(note_name=None) -> None:
        if note_name is None:
            note_name = input("Введите название заметки: ") + '_note.txt'

        with open(f"{note_name}", "w", encoding="utf-8") as note_file:
            print("Введите текст заметки, чтобы прервать ввод введите пустую строку")
            line = stdin.readline()

            while line != '\n':
                note_file.write(line)
                line = stdin.readline()

            print("Ввод завершен\n")
        print(f"Заметка {note_name} создана\n")

    def delete_note(self) -> None:
        requested_note = self.request_note_name_for_delete()
        if path.isfile(requested_note):
            remove(f"{requested_note}")
            print(f"Заметка {requested_note} удалена")
        else:
            self.not_exist_file_warning()
            self.delete_note()

    @staticmethod
    def show_note_content(note_name) -> None:
        with open(f"{note_name}", "r", encoding="utf-8") as note_file:
            for line in note_file:
                print(line.strip())

    @staticmethod
    def show_existing_notes() -> None:
        print("Вам сейчас доступны следующие заметки:")
        folder_path = path.dirname(__file__)
        existing_notes_list = listdir(folder_path)
        for note in [file for file in existing_notes_list if file.endswith('note.txt')]:
            print(note)

    @staticmethod
    def not_exist_file_warning() -> None:
        print("\nЗапрашиваемая заметка отсутствует или введено некорректное название\n")

    @staticmethod
    def request_note_name_for_read() -> str:
        note_name = input("\nВведите название нужной для чтения заметки\n"
                          "(_note.txt будет добавлено автоматически): ")
        return f"{note_name}_note.txt"

    @staticmethod
    def request_note_name_for_edit() -> str:
        note_name = input("\nВведите название нужной для перезаписи заметки\n"
                          "(_note.txt будет добавлено автоматически): ")
        return f"{note_name}_note.txt"

    @staticmethod
    def request_note_name_for_delete() -> str:
        note_name = input("\nВведите название нужной для удаления заметки\n"
                          "(_note.txt будет добавлено автоматически): ")
        return f"{note_name}_note.txt"

    @staticmethod
    def show_menu(choice: str) -> str:
        menu_dict = {'1': 'Создать заметку',
                     '2': 'Прочитать заметку',
                     '3': 'Редактировать заметку',
                     '4': 'Удалить заметку',
                     '5': 'Выйти из меню'}
        return menu_dict[choice]

    @staticmethod
    def request_menu_dict():
        pass


def main() -> None:
    notes_app = NotesApp()
    while True:
        pass
