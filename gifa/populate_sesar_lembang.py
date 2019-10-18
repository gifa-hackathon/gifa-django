import os, django
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gifa.settings")
django.setup()

from dashboard.models import SesarLembang

shp_file = 'datashp/sesar_lembang/sesar_lembang.shp'
ds = DataSource(shp_file)
layer = ds[0]

print(layer.fields)
print(layer.geom_type)

mapping = {
    'id' : 'OID_',
    'polyline': 'LineString25D'
} # The mapping is a dictionary

lm = LayerMapping(SesarLembang, shp_file, mapping)
lm.save(verbose=True) # Save the layermap, imports the data.
