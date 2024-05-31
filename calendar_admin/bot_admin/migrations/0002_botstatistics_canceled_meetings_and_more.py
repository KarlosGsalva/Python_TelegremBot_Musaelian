# Generated by Django 5.0.3 on 2024-05-31 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='botstatistics',
            name='canceled_meetings',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='botstatistics',
            name='edited_meetings',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='botstatistics',
            name='meeting_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
