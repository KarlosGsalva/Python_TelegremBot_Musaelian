from aiogram import Router, Dispatcher
from aiogram_dialog import Dialog, setup_dialogs
from calendar_bot_db.handlers.dialog_choose_dates import (set_calendar_window_for_event,
                                                          edit_event_date_calendar_window,
                                                          set_calendar_window_for_meeting)
from calendar_bot_db.handlers import (create_event, cancel, accept_decline, register, show_published_events,
                                      show_my_calendar, start_cmds, delete_meeting, download_json, show_event,
                                      delete_event, create_meeting, edit_event, end_cap, show_events, publish_events,
                                      download_csv, show_user_meetings, share_event)


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
