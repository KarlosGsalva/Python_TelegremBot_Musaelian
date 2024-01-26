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
            note_name = input("\nВведите название заметки: ") + '_note.txt'

        with open(f"{note_name}", "w", encoding="utf-8") as note_file:
            print("\nВведите текст заметки, чтобы прервать ввод введите пустую строку:")
            line = stdin.readline()

            while line != '\n':
                note_file.write(line)
                line = stdin.readline()

            print("Ввод завершен\n")
        print(f"Заметка {note_name} создана")

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
        print("\nВам сейчас доступны следующие заметки:\n")
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
    def show_menu() -> None:
        menu_dict = {'1': 'Создать заметку',
                     '2': 'Прочитать заметку',
                     '3': 'Редактировать заметку',
                     '4': 'Удалить заметку',
                     '5': 'Выйти из меню'}
        for menu_point, menu_text in menu_dict.items():
            print(f"{menu_point}: {menu_text}")

    def request_command(self):
        print("\nПожалуйста, выберите пункт меню:\n")
        self.show_menu()

        user_choice = input("\nВведите номер команды от 1 до 5: ")
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
                print("Ок, увидимся ;)")
                break
            case _:
                print("\nВы ввели некорректную команду, введите номер от 1 до 5:")


try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
    print("\n\nExiting... работа приложения прекращена командой консоли")
