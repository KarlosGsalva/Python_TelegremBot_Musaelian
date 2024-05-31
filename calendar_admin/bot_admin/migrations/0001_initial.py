# Generated by Django 5.0.3 on 2024-05-28 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('user_count', models.PositiveIntegerField(default=0)),
                ('event_count', models.PositiveIntegerField(default=0)),
                ('edited_events', models.PositiveIntegerField(default=0)),
                ('canceled_events', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'botstatistics',
                'verbose_name_plural': 'botstatistics',
                'db_table': 'botstatistics',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100, unique=True)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField()),
                ('event_details', models.TextField()),
            ],
            options={
                'db_table': 'events',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_tg_id', models.BigIntegerField(unique=True)),
                ('username', models.CharField(max_length=40, null=True)),
                ('email', models.CharField(max_length=40, null=True)),
                ('password_hash', models.CharField(max_length=150, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_name', models.CharField(null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.DurationField(default='00:15:00')),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot_admin.event')),
            ],
            options={
                'verbose_name': 'meeting',
                'verbose_name_plural': 'meetings',
                'db_table': 'meetings',
            },
        ),
        migrations.CreateModel(
            name='MeetingParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CF', 'Confirmed'), ('CL', 'Canceled'), ('PD', 'Pending')], default='PD', max_length=2)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_admin.meeting')),
                ('user', models.ForeignKey(db_column='user_tg_id', on_delete=django.db.models.deletion.CASCADE, to='bot_admin.user', to_field='user_tg_id')),
            ],
            options={
                'db_table': 'meeting_participants',
                'unique_together': {('meeting', 'user')},
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='participants',
            field=models.ManyToManyField(related_name='meetings', through='bot_admin.MeetingParticipant', to='bot_admin.user'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='user_tg_id',
            field=models.ForeignKey(db_column='user_tg_id', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to='bot_admin.user', to_field='user_tg_id'),
        ),
        migrations.AddField(
            model_name='event',
            name='user_tg_id',
            field=models.ForeignKey(db_column='user_tg_id', on_delete=django.db.models.deletion.CASCADE, to='bot_admin.user', to_field='user_tg_id'),
        ),
    ]
