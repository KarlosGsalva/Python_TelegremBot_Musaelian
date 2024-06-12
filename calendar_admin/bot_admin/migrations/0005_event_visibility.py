# Generated by Django 5.0.3 on 2024-06-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot_admin", "0004_meeting_visibility"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="visibility",
            field=models.CharField(
                choices=[("PB", "Published"), ("PR", "Private")],
                default="PR",
                max_length=2,
            ),
        ),
    ]
