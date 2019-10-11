from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _


class Desa(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=_('ID')
    )
    nama = models.CharField(
        max_length=255,
        verbose_name=_('Nama')
    )
    polygon = models.MultiPolygonField(
        null=True,
        blank=True,
        verbose_name=_('Polygon')
    )
    luas = models.DecimalField(
        null=True,
        blank=True,
        max_digits=12,
        decimal_places=4,
        help_text=_('dalam kilometer persegi'),
        verbose_name=_('Luas')
    )
    catatan = models.TextField(
        blank=True,
        verbose_name=_('Catatan')
    )


    class Meta:
        ordering = ['pk']
        get_latest_by = 'pk'
        verbose_name_plural = _('Desa')

    def __unicode__(self):
        return self.nama
