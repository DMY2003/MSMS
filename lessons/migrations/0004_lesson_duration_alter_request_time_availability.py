# Generated by Django 4.1.3 on 2022-11-29 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_lesson_instrument_alter_request_time_availability"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="duration",
            field=models.IntegerField(default=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="request",
            name="time_availability",
            field=models.TimeField(null=True),
        ),
    ]
