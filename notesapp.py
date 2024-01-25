from os import path, listdir
from sys import stdin


class NotesApp:
    def __init__(self) -> None:
        self.note_name = None
        self.note_text = None

    def read_notes(self) -> None:
        self.show_existing_notes()
        requested_note = self.request_note_name()
        if path.isfile(f"{requested_note}"):
            with open(f"{requested_note}", "r", encoding="utf-8") as note_file:
                for line in note_file:
                    print(line.strip())
        else:
            self.not_exist_file_warning()
            self.read_notes()

    def edit_note(self) -> None:
        requested_note = self.request_note_name()
        if path.isfile(requested_note):
            self.show_note_content(requested_note)
            self.create_note(requested_note)
        else:
            self.not_exist_file_warning()

    @staticmethod
    def create_note(note_name=None) -> None:
        if note_name is None:
            note_name = input("Введите название заметки: ")
        with open(f"{note_name}", "w", encoding="utf-8") as note_file:
            print("Введите текст заметки, чтобы прервать ввод введите пустую строку")
            line = stdin.readline()
            while line != '\n':
                note_file.write(line)
                line = stdin.readline()
            print("Ввод завершен")
        print(f"Заметка {note_name}_note.txt создана")

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
        print("Запрашиваемый файл отсутствует или введено некорректное название")

    @staticmethod
    def request_note_name() -> str:
        note_name = input("Введите название нужной для чтения или перезаписи заметки\n"
                          "(_note.txt будет добавлено автоматически): ")
        return f"{note_name}_note.txt"


make_note = NotesApp()
make_note.create_note()
make_note.read_notes()
make_note.edit_note()

