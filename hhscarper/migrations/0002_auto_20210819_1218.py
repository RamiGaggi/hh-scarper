# Generated by Django 3.2.6 on 2021-08-19 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhscarper', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='request',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='request',
            field=models.ManyToManyField(to='hhscarper.Request'),
        ),
    ]
