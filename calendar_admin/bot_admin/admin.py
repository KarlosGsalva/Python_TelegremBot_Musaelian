from django.contrib import admin
from .models import (User, Event, BotStatistics, Meeting,
                     MeetingParticipant, MeetingAdmin)


admin.site.register(MeetingParticipant)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(BotStatistics)
admin.site.register(Meeting, MeetingAdmin)
