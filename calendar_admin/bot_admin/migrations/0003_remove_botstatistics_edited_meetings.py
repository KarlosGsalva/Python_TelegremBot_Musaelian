# Generated by Django 5.0.3 on 2024-05-31 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0002_botstatistics_canceled_meetings_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botstatistics',
            name='edited_meetings',
        ),
    ]