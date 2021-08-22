# Generated by Django 3.2.6 on 2021-08-22 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hhscarper', '0013_delete_skillreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkillReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hhscarper.request')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date of change')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
