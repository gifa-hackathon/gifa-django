from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

from colorfield.fields import ColorField

class ODKConnector(models.Model):
    con_id = models.BigIntegerField(
        primary_key=True,
        validators=[MaxValueValidator(999)],
        verbose_name=_('Connection ID')
    )
    con_nama = models.CharField(
        max_length=255,
        verbose_name=_('Connection Name')
    )
    db_username = models.CharField(
        max_length=255,
        verbose_name=_('DB Username')
    )
    db_password = models.CharField(
        max_length=255,
        verbose_name=_('DB Password')
    )
    db_host = models.CharField(
        max_length=255,
        default='localhost',
        verbose_name=_('DB HOST')
    )
    db_port = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999)],
        default=5432,
        verbose_name=_('DB PORT')
    )
    db_name = models.CharField(
        max_length=255,
        verbose_name=_('DB Name')
    )
    db_schema = models.CharField(
        max_length=255,
        verbose_name=_('DB Schema')
    )
    odk_table_name = models.CharField(
        max_length=255,
        verbose_name=_('ODK Table Name')
    )
    geotrace_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk Garis'),
        verbose_name=_('Geotrace Column')
    )
    geoshape_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk Poligon'),
        verbose_name=_('Geoshape Column')
    )
    geopoint_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk titik'),
        verbose_name=_('Geopoint Column')
    )
    object_color = ColorField(
        default='#213693',
        verbose_name=_('Object Color')
    )
    image_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom untuk gambar, apabila lebih dari satu, gunakan (;) sebagai pemisah'),
        verbose_name=_('Image Column')
    )

    TYPE_CHOICES = (
        ('point', _('point')),
        ('polyline', _('polyline')),
        ('polygon', _('polygon')),
    )
    geometry_type = models.CharField(
        max_length=255,
        choices=TYPE_CHOICES,
        help_text=_('Tipe geometri, satu layer hanya bisa memiliki satu jenis geometri'),
        verbose_name=_('Geometry Type')
    )
    publish = models.BooleanField(
        default=False,
        verbose_name=_('Publish')
    )


    class Meta:
        ordering = ['pk']
        get_latest_by = 'pk'
        verbose_name_plural = _('ODK Connection')

    def __unicode__(self):
        return self.con_id - self.con_nama
