# Generated by Django 2.2.5 on 2019-10-19 18:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20191019_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='BangunanOSM',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255, verbose_name='Nama')),
                ('jenis_bangunan', models.CharField(max_length=255, verbose_name='Connection Name')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326, verbose_name='Polygon')),
            ],
        ),
        migrations.CreateModel(
            name='InfrastrukturJalanOSM',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255, verbose_name='Nama')),
                ('jenis_jalan', models.CharField(max_length=255, verbose_name='Jenis Jalan')),
                ('keterangan', models.CharField(max_length=255, verbose_name='Keterangan')),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326, verbose_name='Polygon')),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]