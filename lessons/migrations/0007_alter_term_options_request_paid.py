# Generated by Django 4.1.3 on 2022-12-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_term'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ('start_date',)},
        ),
        migrations.AddField(
            model_name='request',
            name='paid',
            field=models.IntegerField(default=0),
        ),
    ]
