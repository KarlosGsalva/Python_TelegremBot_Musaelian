from os import path
from sys import stdin


class NotesApp:
    def __init__(self) -> None:
        self.note_name = input("Введите название заметки: ")
        self.note_text = None

    def create_note(self) -> None:
        with open(f"{self.note_name}_note.txt", "w", encoding="utf-8") as note_file:
            line = stdin.readline()
            for line in self.note_text:
                notes_file.writelines(line)
        print(f"Заметка {self.note_name} создана")

    def read_notes(self) -> None:
        self.show_existing_notes()
        output_note = input("Введите название необходимой: ")
        if path.isfile(f"{output_note}.txt"):
            with open(f"{output_note}.txt", "r", encoding="utf-8") as note_file:
                for line in note_file:
                    print(line.strip())
        else:
            print("Запрашиваемый файл отсутствует или введено некорректное название")
            self.read_notes()

    @staticmethod
    def show_existing_notes() -> None:
        print("Вам сейчас доступны следующие заметки:")
        folder_path = path.dirname(__file__)
        existing_notes_list = os.listdir(folder_path)
        for note in [file for file in existing_notes_list if file.endswith('note.txt')]:
            print(note)


make_note = NotesApp()
make_note.build_note()
make_note.read_notes()

