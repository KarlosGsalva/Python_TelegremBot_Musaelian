from django.contrib import admin
from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class User(models.Model):
    user_tg_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=40, null=True)
    email = models.CharField(max_length=40, null=True)
    password_hash = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.user_tg_id)


class Event(models.Model):
    user_tg_id = models.ForeignKey(User,
                                   to_field="user_tg_id",
                                   db_column="user_tg_id",
                                   on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100, unique=True)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_details = models.TextField()

    class Meta:
        db_table = "events"

    def __str__(self):
        return self.event_name


class BotStatistics(models.Model):
    date = models.DateField()
    user_count = models.PositiveIntegerField(default=0)
    event_count = models.PositiveIntegerField(default=0)
    edited_events = models.PositiveIntegerField(default=0)
    canceled_events = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "botstatistics"
        verbose_name = "botstatistics"
        verbose_name_plural = "botstatistics"

    def __str__(self):
        return str(self.date)


class Meeting(models.Model):
    user_tg_id = models.ForeignKey(User,
                                   to_field="user_tg_id",
                                   db_column="user_tg_id",
                                   on_delete=models.CASCADE,
                                   related_name="organizer",
                                   default=1)
    participants = models.ManyToManyField(User, related_name="meetings", through="MeetingParticipant")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    meeting_name = models.CharField(null=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField(default="00:15:00")
    end_time = models.TimeField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "meetings"
        verbose_name = "meeting"
        verbose_name_plural = "meetings"

    def __str__(self):
        return f"{self.meeting_name} on {self.date} at {self.time}"


class MeetingParticipant(models.Model):
    class MeetingStatus(models.TextChoices):
        CONFIRMED = "CF", "Confirmed"
        CANCELED = "CL", "Canceled"
        PENDING = "PD", "Pending"

    meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             to_field='user_tg_id',
                             db_column='user_tg_id',
                             on_delete=models.CASCADE)
    status = models.CharField(max_length=2,
                              choices=MeetingStatus.choices,
                              default=MeetingStatus.PENDING)

    class Meta:
        db_table = "meeting_participants"
        unique_together = ('meeting', 'user')


class MeetingParticipantInline(admin.TabularInline):
    model = MeetingParticipant
    extra = 1
    can_delete = True
    show_change_link = True
    readonly_fields = ('user', 'status')
    fields = ('user', 'status')


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('meeting_name', 'date', 'time', 'duration', 'end_time', 'details')
    inlines = [MeetingParticipantInline]
