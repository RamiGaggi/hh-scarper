# Generated by Django 3.2.6 on 2021-08-13 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhscarper', '0008_alter_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='keyword',
            field=models.CharField(max_length=100, verbose_name='ключевое слово'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='external_id',
            field=models.IntegerField(),
        ),
    ]