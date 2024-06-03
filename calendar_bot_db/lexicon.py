MENU = {"/start": "Начать работу",
        "/1": "Создать событие",
        "/2": "Вывести подробности события",
        "/3": "Изменить данные события",
        "/4": "Удалить событие",
        "/5": "Показать все события",
        "/6": "Регистрация",
        "/7": "Создать встречу",
        "/8": "Показать назначенные встречи",
        "/9": "Удалить встречу",
        "/10": "Показать календарь",
        "/11": "Поделиться событием",
        "/12": "Опубликовать события",
        "/13": "Показать публичные события",
        "/14": "Выгрузить события в json",
        "/15": "Выгрузить события в csv"}


MODES = {}
WARNING_TEXTS = {
        "hello": "Здравствуйте, для начала работы выберите пункт меню:",
        "show_menu": "\n".join(f"{com}: {des}" for com, des in MENU.items()),
        "request_event_name": "Пожалуйста, введите название нового события:",
        "request_event_date": "Пожалуйста, выберите дату события",
        "request_event_time": "Пожалуйста, введите время события:",
        "request_event_details": "Пожалуйста, введите описание к событию\n"
                                 "или оставьте прочерк '-':",
        "request_meeting_name": "Пожалуйста, введите название новой встречи:",
        "request_meeting_date": "Пожалуйста, выберите дату встречи",
        "request_meeting_time": "Пожалуйста, введите время встречи:",
        "request_meeting_duration": "Пожалуйста, введите длительность встречи в минутах, "
                                    "например: 15, 30, 90 и тд или нажмите отмену:",
        "duration_warning": "Вы ввели некорректное значение длительности встречи",
        "request_meeting_participants": "Пожалуйста, выберите участников встречи:",
        "request_shared_participant": "Пожалуйста, выберите участников для отправки события:",
        "request_meeting_details": "Пожалуйста, введите описание к встрече\n"
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
        "request_meeting_for_delete": "Выберите встречу для удаления:",
        "show_event": "Пожалуйста, данные события",
        "show_all_events": "Пожалуйста, все доступные события:",
        "share_event": "Пожалуйста, выберие событие которым хотите поделиться:",
        "event_made": "Событие создано.",
        "meeting_made": "Встреча создана.",
        "request_username": "Введите Ваше имя пользователя:",
        "request_email": "Введите Ваш email:",
        "request_password": "Введите Ваш пароль:",
        "choose_for_publish": "Выберите события для публикации",
        "events_published": "Выбранные события опубликованы",
        "show_published_events": "Пожалуйста, открытые события:",
        "watch_json": "Для просмотра json перейдите по ссылке, нажав на кнопку",
        "data_saved": "Ваши данные сохранены.",
        "exit": "Вы вышли из приложения\n\n"
                "Чтобы снова приступить к работе введите команду /start\n"
                "или выберите пункт меню.",
        "cancel": "Отменять нечего, для продолжения работы, выберите пункт меню.",
        "calendar": "Для просмотра календаря в браузере, нажмите на кнопку\n 'Мой календарь' "
                    "и перейдите по ссылке.\n\n"
                    "Для получения расписания в чате, нажмите на кнопку 'Вывести расписание в чат', ",
}
