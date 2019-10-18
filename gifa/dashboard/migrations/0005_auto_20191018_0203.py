# Generated by Django 2.2.5 on 2019-10-18 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_intensitasgempa_rendamanbanjir_sesarlembang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intensitasgempa',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=4, help_text='dalam SR', max_digits=25, null=True, verbose_name='value'),
        ),
    ]
