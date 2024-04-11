from django.contrib import admin
from .models import User, Event, BotStatistics


admin.site.register(User)
admin.site.register(Event)
admin.site.register(BotStatistics)
