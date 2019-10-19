from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator



class MapServices(models.Model):
    service_id = models.BigIntegerField(
        primary_key=True,
        validators=[MaxValueValidator(999)],
        verbose_name=_('Service ID')
    )
    service_name = models.CharField(
        max_length=255,
        verbose_name=_('Service Name')
    )
    description = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('Description')
    )
    service_attribution = models.CharField(
        max_length=255,
        verbose_name=_('Service Attribution')
    )
    service_url = models.CharField(
        max_length=255,
        verbose_name=_('WMS URL')
    )
    publish = models.BooleanField(
        default=False,
        verbose_name=_('Publish')
    )


class LayerServices(models.Model):
    map_services = models.ForeignKey(
        MapServices,
        verbose_name=_('Map Service'),
        related_name='layerservices',
        on_delete=models.CASCADE,

    )
    layer_name = models.CharField(
        max_length=255,
        verbose_name=_('Layer Name')
    )
    layer_display_name = models.CharField(
        max_length=255,
        verbose_name=_('Layer Display Name')
    )
