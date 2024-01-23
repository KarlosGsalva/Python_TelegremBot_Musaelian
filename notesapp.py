from os import path


class NotesApp:
    def __init__(self) -> None:
        self.note_text = input("Пожалуйста, введите текст заметки: ")
        self.note_name = input("Пожалуйста, введите название заметки: ")
        self.notes_list = []

    def build_note(self) -> None:
        self.notes_list.append(self.note_name)
        with open(f"{self.note_name}.txt", "w", encoding="utf-8") as notes_file:
            notes_file.write(self.note_text)
        print(f"Заметка {self.note_name} создана")

    def read_notes(self) -> None:
        print("Вам сейчас доступны следующие заметки:")
        for note_name in self.notes_list:
            print(note_name)
        output_note = input("Введите название необходимой: ")
        if path.isfile(f"{output_note}.txt"):
            with open(f"{output_note}.txt", "r", encoding="utf-8") as note_file:
                for line in note_file:
                    print(line.strip())
        else:
            print("Запрашиваемый файл отсутствует или введено некорректное название")
            self.read_notes()


make_note = NotesApp()
make_note.build_note()
make_note.read_notes()

