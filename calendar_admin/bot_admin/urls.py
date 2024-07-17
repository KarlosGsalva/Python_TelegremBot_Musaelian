from django.urls import path, include
from rest_framework import routers
from .views import (
    show_user_calendar,
    export_events_csv,
    export_events_json,
    UserViewSet,
    MeetingViewSet,
    EventViewSet,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"events", EventViewSet, basename="event")
router.register(r"meetings", MeetingViewSet, basename="meeting")

urlpatterns = [
    path("api/", include(router.urls)),
    path("calendar/", show_user_calendar, name="user_calendar"),
    path("export/csv/", export_events_csv, name="export_events_csv"),
    path("export/json/", export_events_json, name="export_events_json"),
]
