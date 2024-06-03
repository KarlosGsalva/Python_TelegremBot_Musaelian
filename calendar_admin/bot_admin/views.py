import csv
import hashlib
import hmac
import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import User, Event, Meeting

logger = logging.getLogger(__name__)


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


def export_events_csv(request):
    user_id = request.GET.get('id')
    if not user_id:
        logger.error("Missing user_id parameter")
        return HttpResponse(status=400, content="Missing user_id parameter")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="events.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    try:
        writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Type", "Name", "Date", "Time", "Details", "Visibility"])

        events = Event.objects.filter(user_tg_id=user_id)
        meetings = Meeting.objects.filter(user_tg_id=user_id)

        for event in events:
            writer.writerow([
                'Event',
                event.event_name,
                event.event_date.strftime('%Y-%m-%d'),
                event.event_time.strftime('%H:%M:%S'),
                event.event_details,
                event.visibility
            ])

        for meeting in meetings:
            writer.writerow([
                'Meeting',
                meeting.meeting_name,
                meeting.date.strftime('%Y-%m-%d'),
                meeting.time.strftime('%H:%M:%S'),
                meeting.details,
                meeting.visibility
            ])

        return response

    except Exception as e:
        logger.error(f"An error occurred while exporting events to CSV: {e}")
        return HttpResponse(status=500, content="An error occurred while exporting events")


def export_events_json(request):
    try:
        user_id = request.GET.get('id')
        if not user_id:
            return HttpResponse(status=400, content="Missing user_id parameter")

        events = Event.objects.filter(user_tg_id=user_id)
        meetings = Meeting.objects.filter(user_tg_id=user_id)

        events_data = []
        for event in events:
            events_data.append({
                'type': 'Event',
                'name': event.event_name,
                'date': event.event_date.strftime('%Y-%m-%d'),
                'time': event.event_time.strftime('%H:%M:%S'),
                'details': event.event_details,
                'visibility': event.visibility
            })

        for meeting in meetings:
            events_data.append({
                'type': 'Meeting',
                'name': meeting.meeting_name,
                'date': meeting.date.strftime('%Y-%m-%d'),
                'time': meeting.time.strftime('%H:%M:%S'),
                'details': meeting.details,
                'visibility': meeting.visibility
            })

        return JsonResponse(events_data, safe=False)
    except Exception as e:
        logger.error(f"An error occurred while exporting events to json: {e}")
        return HttpResponse(status=500, content="An error occurred while exporting json events")
