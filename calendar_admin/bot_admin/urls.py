from django.urls import path
from .views import show_user_calendar, export_events_csv, export_events_json

urlpatterns = [
    path("calendar/", show_user_calendar, name="user_calendar"),
    path('export/csv/', export_events_csv, name='export_events_csv'),
    path('export/json/', export_events_json, name='export_events_json'),
]
