# Generated by Django 3.2.6 on 2021-08-09 16:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hhscarper', '0002_vacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 8, 9, 16, 59, 23, 181378, tzinfo=utc), verbose_name='date of creation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vacancy',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date of change'),
        ),
    ]