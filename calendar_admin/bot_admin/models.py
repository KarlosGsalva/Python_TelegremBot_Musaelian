from django.db import models


class User(models.Model):
    user_tg_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password_hash = models.CharField(max_length=150)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return str(self.user_tg_id)


class Event(models.Model):
    user_tg_id = models.OneToOneField(User, to_field='user_tg_id',
                                      db_column='user_tg_id',
                                      on_delete=models.CASCADE)
    event_name = models.CharField(unique=True)
    event_date = models.DateField(auto_now_add=True)
    event_time = models.TimeField(auto_now_add=True)
    event_details = models.TextField()

    class Meta:
        db_table = 'events'

    def __str__(self):
        return self.event_name
