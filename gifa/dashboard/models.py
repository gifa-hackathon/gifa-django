from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from odkcollect.models import ODKConnector
import django_tables2 as tables


class BangunanOSM(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=_('ID')
    )
    nama = models.CharField(
        max_length=255,
        verbose_name=_('Nama')
    )
    jenis_bangunan = models.CharField(
        max_length=255,
        verbose_name=_('Connection Name')
    )
    polygon = models.MultiPolygonField(
        null=True,
        blank=True,
        verbose_name=_('Polygon')
    )


class InfrastrukturJalanOSM(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=_('ID')
    )
    nama = models.CharField(
        max_length=255,
        verbose_name=_('Nama')
    )
    jenis_jalan = models.CharField(
        max_length=255,
        verbose_name=_('Jenis Jalan')
    )
    keterangan = models.CharField(
        max_length=255,
        verbose_name=_('Keterangan')
    )
    polyline = models.MultiLineStringField(
        null=True,
        blank=True,
        verbose_name=_('Polyline')
    )


class SesarLembang(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=_('ID')
    )
    polyline = models.MultiLineStringField(
        null=True,
        blank=True,
        verbose_name=_('Polyline')
    )


class IntensitasGempa(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=_('ID')
    )
    polygon = models.MultiPolygonField(
        null=True,
        blank=True,
        verbose_name=_('Polygon')
    )
    luas = models.DecimalField(
        null=True,
        blank=True,
        max_digits=25,
        decimal_places=4,
        help_text=_('dalam meter persegi'),
        verbose_name=_('Luas')
    )
    value = models.DecimalField(
        null=True,
        blank=True,
        max_digits=25,
        decimal_places=4,
        help_text=_('dalam SR'),
        verbose_name=_('value')
    )


class RendamanBanjir(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=_('ID')
    )
    polygon = models.MultiPolygonField(
        null=True,
        blank=True,
        verbose_name=_('Polygon')
    )
    luas = models.DecimalField(
        null=True,
        blank=True,
        max_digits=25,
        decimal_places=4,
        help_text=_('dalam meter persegi'),
        verbose_name=_('Luas')
    )


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
        max_digits=25,
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


class Category(models.Model):
    category_name = models.CharField(
        max_length=255,
        verbose_name=_('Category Name')
    )
    odk_connections = models.ManyToManyField(
        ODKConnector,
        verbose_name=_('ODK Conncetions List ID'),
    )


    class Meta:
        ordering = ['pk']
        get_latest_by = 'pk'
        verbose_name_plural = _('Category')

    def __unicode__(self):
        return self.category_name
