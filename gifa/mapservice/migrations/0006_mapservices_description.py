# Generated by Django 2.2.5 on 2019-10-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapservice', '0005_auto_20191018_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapservices',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
    ]
