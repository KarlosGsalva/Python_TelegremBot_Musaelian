from aiogram import Router, Dispatcher
from aiogram_dialog import Dialog, setup_dialogs
from calendar_bot_db.handlers.dialog_choose_dates import (set_calendar_window_for_event,
                                                          edit_event_date_calendar_window,
                                                          set_calendar_window_for_meeting)
from calendar_bot_db.handlers import (start_cmds, show_event, show_events,
                                      register, create_event, edit_event,
                                      delete_event, cancel, end_cap,
                                      create_meeting, accept_decline, show_user_meetings,
                                      show_my_calendar, delete_meeting, share_event,
                                      publish_events, show_published_events, download_json,
                                      download_csv)


def get_routers(dp: Dispatcher) -> list[Router]:
    # Регистрируем окно в диалоге
    dialog_date_event_state = Dialog(set_calendar_window_for_event)
    dialog_date_meeting_state = Dialog(set_calendar_window_for_meeting)
    dialog_edit_date_state = Dialog(edit_event_date_calendar_window)

    # Инициализация DialogManager
    setup_dialogs(dp)

    return [
        dialog_date_event_state,
        dialog_date_meeting_state,
        dialog_edit_date_state,
        start_cmds.router,
        cancel.router,
        download_json.router,
        download_csv.router,
        show_published_events.router,
        publish_events.router,
        share_event.router,
        show_my_calendar.router,
        delete_meeting.router,
        show_user_meetings.router,
        accept_decline.router,
        create_meeting.router,
        show_events.router,
        show_event.router,
        register.router,
        create_event.router,
        edit_event.router,
        delete_event.router,
        end_cap.router
    ]
