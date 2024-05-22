from django.db import models
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class User(models.Model):
    user_tg_id = models.IntegerField(unique=True)
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
    event_name = models.CharField(unique=True)
    event_date = models.DateField(auto_now_add=True)
    event_time = models.TimeField(auto_now_add=True)
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
    class MeetingStatus(models.TextChoices):
        CONFIRMED = "CF", "Confirmed"
        CANCELED = "CL", "Canceled"
        PENDING = "PD", "Pending"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    planner = models.CharField()
    participants = models.CharField()
    status = models.CharField(max_length=3,
                              choices=MeetingStatus.choices,
                              default=MeetingStatus.PENDING)

    class Meta:
        db_table = "meeting"
        verbose_name = "meeting"
        verbose_name_plural = "meetings"

    def __str__(self):
        return (f"{self.user.username} - {self.event.event_name}"
                f"{self.date} - {self.time}")
