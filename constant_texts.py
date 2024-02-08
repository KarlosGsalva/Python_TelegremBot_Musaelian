MENU_TEXT: dict = {"/1": "Создать заметку",
                   "/2": "Прочитать заметку",
                   "/3": "Редактировать заметку",
                   "/4": "Удалить заметку",
                   "/5": "Показать отсортированные по длинне заметки",
                   "/6": "Выйти из меню",
                   "/start": "start",
                   "/cancel": "выйти из приложения"}

NOTIFICATION_TEXTS: dict = {"choice_menu_point": "\nПожалуйста, выберите пункт меню:\n",
                            "enter_menu_point": "\nВведите номер команды от 1 до 6: ",
                            "incorrect_menu_point": "\nВы ввели некорректную команду, введите номер от 1 до 5:",
                            "request_note_delete": "\nВведите название нужной для удаления заметки\n"
                                                   "(_note.txt будет добавлено автоматически): ",
                            "request_note_edit": "\nВведите название нужной для перезаписи заметки\n"
                                                 "(_note.txt будет добавлено автоматически): ",
                            "request_note_read": "\nВведите название нужной для чтения заметки\n"
                                                 "(_note.txt будет добавлено автоматически): ",
                            "note_not_exist": "\nЗапрашиваемая заметка отсутствует или введено некорректное название\n",
                            "accessed_notes": "\nВам сейчас доступны следующие заметки:\n",
                            "incorrect_note_name": "Вы ввели некорректное название заметки\n\n"
                                                   "Пожалуйста, попробуйте еще раз\n\n"
                                                   "Если вы хотите прервать ввод, отправьте команду\n"
                                                   "/cancel",
                                              "enter_finished": "Ввод завершен\n",
                            "request_note_text": "\nВведите текст заметки, чтобы прервать ввод введите /cancel:",
                            "request_note_name": "\nВведите название заметки: ",
                            "bye": "Ок, увидимся ;)",
                            "sorted_notes": "Пожалуйста, имеющиеся заметки в упорядоченном виде: \n",
                            "error": "Произошла ошибка",
                            "hello": "Здравствуйте, чтобы поработать с заметками выберите пункт меню \n",
                            "help": "Я умею следующие штуки: \n",
                            "cancel": "Отменять нечего, вы еще не выбрали ни один пункт меню\n\n"
                                      "Чтобы продолжить выберите пункт меню",
                            "exit": "Вы вышли из приложения\n\n"
                                    "Чтобы снова приступить к работе введите команду /start",
                            "note_created": "Заявка создана.",
                            "menu": "\n".join(f"{key}: {value}" for key, value in MENU_TEXT.items())}
