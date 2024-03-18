MENU = {"/start": "Начать работу",
        "/1": "Создать событие",
        "/2": "Вывести подробности события",
        "/3": "Изменить данные события",
        "/4": "Удалить событие",
        "/5": "Показать все события"}

MODES = {}
WARNING_TEXTS = {
        "hello": "Здравствуйте, для начала работы выберите пункт меню:",
        "show_menu": "\n".join(f"{com}: {des}" for com, des in MENU.items()),
        "request_event_name": "Пожалуйста, введите название нового события:",
        "request_event_date": "Пожалуйста, выберите дату события",
        "request_event_time": "Пожалуйста, введите время события:",
        "request_event_details": "Пожалуйста, введите описание к событию\n"
                                 "или оставьте прочерк '-':",
        "request_event_for_show": "Пожалуйста, выберите событие для чтения",
        "request_event_for_edit": "Выберите событие для изменения:",
        "request_event_point_for_edit": "Выберие пункт изменений:",
        "request_new_event_name": "Введите новое название события:",
        "event_name_edited": "Название события изменено.",
        "event_date_edited": "Дата события изменена.",
        "request_new_event_time": "Выберите или введите новое время события:",
        "event_time_edited": "Время события изменено.",
        "request_new_event_details": "Введите новое описание события:",
        "event_details_edited": "Описание события изменено.",
        "request_event_for_delete": "Выберите событие для удаления:",
        "show_event": "Пожалуйста, данные события",
        "show_all_events": "Пожалуйста, все доступные события:",
        "event_made": "Событие создано.",
        "exit": "Вы вышли из приложения\n\n"
                "Чтобы снова приступить к работе введите команду /start\n"
                "или выберите пункт меню.",
        "cancel": "Отменять нечего, для продолжения работы, выберите пункт меню.",

}