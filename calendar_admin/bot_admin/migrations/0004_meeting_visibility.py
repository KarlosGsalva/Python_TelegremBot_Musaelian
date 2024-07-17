# Generated by Django 5.0.3 on 2024-06-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot_admin", "0003_remove_botstatistics_edited_meetings"),
    ]

    operations = [
        migrations.AddField(
            model_name="meeting",
            name="visibility",
            field=models.CharField(
                choices=[("PB", "Published"), ("PR", "Private")],
                default="PR",
                max_length=2,
            ),
        ),
    ]
