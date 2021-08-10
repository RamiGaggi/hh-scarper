# Generated by Django 3.2.6 on 2021-08-09 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhscarper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.IntegerField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name': 'vacancy',
                'verbose_name_plural': 'vacancies',
            },
        ),
    ]
