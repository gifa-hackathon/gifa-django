# Generated by Django 2.2.5 on 2019-10-19 18:39

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20191019_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infrastrukturjalanosm',
            name='polygon',
        ),
        migrations.AddField(
            model_name='infrastrukturjalanosm',
            name='polyline',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=4326, verbose_name='Polyline'),
        ),
    ]