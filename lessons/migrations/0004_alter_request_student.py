# Generated by Django 4.1.3 on 2022-12-02 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0003_alter_request_student"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="lessons.student"
            ),
        ),
    ]