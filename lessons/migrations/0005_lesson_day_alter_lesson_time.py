# Generated by Django 4.1.3 on 2022-11-30 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0004_lesson_duration_alter_request_time_availability"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="day",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="lesson", name="time", field=models.TimeField(null=True),
        ),
    ]