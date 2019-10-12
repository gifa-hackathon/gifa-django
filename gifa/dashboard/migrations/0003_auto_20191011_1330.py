# Generated by Django 2.2.5 on 2019-10-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odkcollect', '0002_auto_20191011_1123'),
        ('dashboard', '0002_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='odk_connections',
        ),
        migrations.AddField(
            model_name='category',
            name='odk_connections',
            field=models.ManyToManyField(to='odkcollect.ODKConnector', verbose_name='ODK Conncetions List ID'),
        ),
    ]
