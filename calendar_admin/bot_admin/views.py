import hashlib
import hmac
import time
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as AuthUser
from .models import User, Event, Meeting


def show_user_calendar(request):
    user_tg_id = request.GET.get('id')

    # Получаем или создаем пользователя
    user = get_object_or_404(User, user_tg_id=user_tg_id)

    # Получаем события пользователя
    events = list(Event.objects.filter(user_tg_id=user_tg_id))

    # Получаем встречи пользователя
    meetings = list(Meeting.objects.filter(user_tg_id=user_tg_id))

    combined_list = sorted(events + meetings, key=lambda x: (
        x.event_date if isinstance(x, Event) else x.date, x.event_time
        if isinstance(x, Event) else x.time))

    return render(request, "calendar.html", {"combined_list": combined_list})
