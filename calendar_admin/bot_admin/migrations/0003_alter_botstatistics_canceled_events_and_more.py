# Generated by Django 5.0.3 on 2024-04-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_admin', '0002_botstatistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botstatistics',
            name='canceled_events',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='botstatistics',
            name='edited_events',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='botstatistics',
            name='event_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='botstatistics',
            name='user_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
