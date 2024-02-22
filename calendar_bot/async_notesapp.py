from aiogram.utils.keyboard import InlineKeyboardButton
import aiofiles
import aiofiles.os
import asyncio

from os import path, listdir

from constant_texts import MENU_TEXT, NOTIFICATION_TEXTS


class AsyncNotesApp:
    def __init__(self) -> None:
        self.note_name = None
        self.note_text = None
        self.MENU_TEXT: dict = MENU_TEXT
        self.NOTIFICATIONS: dict = NOTIFICATION_TEXTS

    async def create_note(self, note_name, note_text) -> None:
        try:
            async with aiofiles.open(f"{note_name}_note.txt", "a", encoding="utf-8") as note_file:
                await note_file.write(note_text)
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    async def read_note(self, note) -> str | None:
        try:
            async with aiofiles.open(note, "r", encoding="utf-8") as note_file:
                note_text = await note_file.read()
                return note_text
        except Exception as e:
            print(self.NOTIFICATIONS["error_read"], e)
            return None

    async def edit_note(self, note_name, note_text) -> None:
        try:
            async with aiofiles.open(note_name, "w", encoding="utf-8") as note_file:
                await note_file.write(note_text)
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    async def delete_note(self, note) -> None:
        try:
            await aiofiles.os.remove(note)
        except Exception as e:
            print(self.NOTIFICATIONS["error"], e)

    # Создаем кнопки для демонстрации отсортированных заметок
    async def notes_in_inline_buttons(self, order=True) -> list:
        buttons_list: list[InlineKeyboardButton] = []
        if order:
            notes: list = await self.sort_notes()
            for note in notes:
                buttons_list.append(InlineKeyboardButton(text=f"Заметка {note[:-9]}",
                                                         callback_data=f"show_note_{note}"))
        else:
            for note in self.gather_all_notes():
                buttons_list.append(InlineKeyboardButton(text=f"Заметка {note[:-9]}",
                                                         callback_data=f"show_note_{note}"))
        return buttons_list

    async def sort_notes(self) -> list | None:
        try:
            notes: dict = await self._make_dict_for_sort_notes()
            sorted_notes = sorted(notes.items(), key=lambda note: note[1], reverse=True)
            sorted_note_names = [note[0] for note in sorted_notes]
            return sorted_note_names
        except Exception as e:
            print("Произошла ошибка", e)
            return None

    async def _make_dict_for_sort_notes(self) -> dict | None:
        try:
            notes_len: dict = {}
            notes = await asyncio.to_thread(lambda: self.gather_all_notes())
            for note in notes:
                async with aiofiles.open(note, "r", encoding="utf-8") as note_file:
                    text_file = await note_file.read()
                    notes_len[note] = len(text_file)
            return notes_len
        except Exception as e:
            print("Произошла ошибка", e)
            return None

    # Собираем список заметок из текущей директории, если директория не указана
    @staticmethod
    def gather_all_notes(main_path=None) -> list:
        try:
            if main_path is None:
                main_path = path.dirname(__file__)
            result = [note for note in listdir(main_path) if note.endswith("note.txt")]
            return result
        except Exception as e:
            print("Произошла ошибка", e)
            return []
