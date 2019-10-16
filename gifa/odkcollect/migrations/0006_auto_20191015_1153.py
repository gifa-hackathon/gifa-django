# Generated by Django 2.2.5 on 2019-10-15 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odkcollect', '0005_auto_20191014_1244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='odkconnector',
            name='latitude_column',
        ),
        migrations.RemoveField(
            model_name='odkconnector',
            name='longitude_column',
        ),
        migrations.RemoveField(
            model_name='odkconnector',
            name='polygon_column',
        ),
        migrations.RemoveField(
            model_name='odkconnector',
            name='polyline_column',
        ),
        migrations.AddField(
            model_name='odkconnector',
            name='geopoint_column',
            field=models.CharField(blank=True, help_text='Kolom Geometri untuk titik', max_length=255, null=True, verbose_name='Geopoint Column'),
        ),
        migrations.AddField(
            model_name='odkconnector',
            name='geoshape_column',
            field=models.CharField(blank=True, help_text='Kolom Geometri untuk Poligon', max_length=255, null=True, verbose_name='Geoshape Column'),
        ),
        migrations.AddField(
            model_name='odkconnector',
            name='geotrace_column',
            field=models.CharField(blank=True, help_text='Kolom Geometri untuk Garis', max_length=255, null=True, verbose_name='Geotrace Column'),
        ),
        migrations.AddField(
            model_name='odkconnector',
            name='image_column',
            field=models.CharField(blank=True, help_text='Kolom untuk gambar, apabila lebih dari satu, gunakan (;) sebagai pemisah', max_length=255, null=True, verbose_name='Image Column'),
        ),
        migrations.AlterField(
            model_name='odkconnector',
            name='geometry_type',
            field=models.CharField(choices=[('point', 'point'), ('polyline', 'polyline'), ('polygon', 'polygon')], help_text='Tipe geometri, satu layer hanya bisa memiliki satu jenis geometri', max_length=255, verbose_name='Geometry Type'),
        ),
    ]