from django.urls import path
from .views import show_user_calendar

urlpatterns = [
    path("calendar/", show_user_calendar, name="user_calendar"),

]
