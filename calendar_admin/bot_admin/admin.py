from django.contrib import admin
from .models import User, Event, BotStatistics, Meeting, MeetingParticipant


admin.site.register(MeetingParticipant)
admin.site.register(Meeting)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(BotStatistics)
