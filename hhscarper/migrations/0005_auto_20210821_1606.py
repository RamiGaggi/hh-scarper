# Generated by Django 3.2.6 on 2021-08-21 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hhscarper', '0004_auto_20210821_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='VacancyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hhscarper.request')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hhscarper.vacancy')),
            ],
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='request',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='request',
            field=models.ManyToManyField(through='hhscarper.VacancyRequest', to='hhscarper.Request'),
        ),
    ]