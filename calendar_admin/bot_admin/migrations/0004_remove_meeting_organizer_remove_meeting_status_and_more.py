# Generated by Django 5.0.3 on 2024-05-27 20:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0003_meeting_user_tg_id_alter_meeting_organizer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='organizer',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='status',
        ),
        migrations.AddField(
            model_name='meetingparticipant',
            name='status',
            field=models.CharField(choices=[('CF', 'Confirmed'), ('CL', 'Canceled'), ('PD', 'Pending')], default='PD', max_length=2),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='user_tg_id',
            field=models.ForeignKey(db_column='user_tg_id', default=1, on_delete=django.db.models.deletion.CASCADE, related_name='organizer', to='bot_admin.user', to_field='user_tg_id'),
        ),
    ]
