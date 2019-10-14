from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

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
    polyline_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk Garis'),
        verbose_name=_('Polyline Column')
    )
    polygon_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk Poligon'),
        verbose_name=_('Polygon Column')
    )
    latitude_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk titik'),
        verbose_name=_('Latitude Column')
    )
    longitude_column = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Kolom Geometri untuk titik'),
        verbose_name=_('Longitude Column')
    )

    TYPE_CHOICES = (
        ('point', _('point')),
        ('polyline', _('polyline')),
        ('polygon', _('polygon')),
    )
    geometry_type = models.CharField(
        max_length=255,
        choices=TYPE_CHOICES,
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
